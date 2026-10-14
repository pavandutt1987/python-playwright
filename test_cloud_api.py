import asyncio
import json
import os
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request

from websockets.asyncio.client import connect
from websockets.exceptions import InvalidStatus


class CloudAPITests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0))
            cls.port = sock.getsockname()[1]
        cls.http = f"http://127.0.0.1:{cls.port}"
        cls.ws = f"ws://127.0.0.1:{cls.port}/ws/run"
        cls.origin = "https://studio.test"
        env = dict(os.environ, PLAYWRIGHT_STUDIO_DB=str(Path(cls.temp.name) / "history.db"),
                   STUDIO_PUBLIC_ORIGIN=cls.origin, STUDIO_REMOTE_DESKTOP="1",
                   STUDIO_MAX_RUNS="1", PYTHONDONTWRITEBYTECODE="1")
        cls.process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app.server:app", "--host", "127.0.0.1",
             "--port", str(cls.port)], env=env, stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for _ in range(100):
            try:
                with urllib.request.urlopen(cls.http + "/api/health", timeout=0.2):
                    return
            except (OSError, urllib.error.URLError):
                time.sleep(0.1)
        cls.process.terminate()
        cls.process.wait(timeout=5)
        cls.temp.cleanup()
        raise RuntimeError("Test API did not start")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate()
        cls.process.wait(timeout=10)
        cls.temp.cleanup()

    def get_json(self, path):
        with urllib.request.urlopen(self.http + path, timeout=10) as response:
            return json.load(response)

    async def execute(self, payload):
        async with connect(self.ws, origin=self.origin) as ws:
            await ws.send(json.dumps(payload))
            messages = []
            async for raw in ws:
                item = json.loads(raw)
                messages.append(item)
                if item.get("type") == "done":
                    return messages

    async def test_desktop_configuration_and_demo(self):
        status = await asyncio.to_thread(self.get_json, "/api/status")
        self.assertTrue(status["remote_desktop"])
        self.assertTrue(status["tsx"])
        self.assertIn("path=desktop/websockify", status["desktop_url"])
        demo = await asyncio.to_thread(self.get_json, "/api/templates/headed_demo?lang=python")
        self.assertIn("HEADED", demo["code"])

    async def test_run_saved_before_completion(self):
        messages = await self.execute({"language": "python", "code": "print('api smoke')"})
        self.assertEqual(messages[-1]["status"], "success")
        history = await asyncio.to_thread(self.get_json, "/api/history")
        self.assertIn("api smoke", history[0]["output"])

    async def test_invalid_payload_rejected(self):
        messages = await self.execute({"language": "shell", "code": "anything"})
        self.assertEqual(messages[-1]["status"], "failed")
        self.assertTrue(any("Unsupported language" in m.get("text", "") for m in messages))

    async def test_foreign_websocket_origin_rejected(self):
        with self.assertRaises(InvalidStatus):
            async with connect(self.ws, origin="https://other.test"):
                self.fail("Foreign origin was accepted")

    async def test_foreign_write_origin_rejected(self):
        def post():
            request = urllib.request.Request(self.http + "/api/stop", data=b'{}',
                headers={"Content-Type": "application/json", "Origin": "https://other.test"})
            with urllib.request.urlopen(request):
                pass
        with self.assertRaises(urllib.error.HTTPError) as caught:
            await asyncio.to_thread(post)
        self.assertEqual(caught.exception.code, 403)
        caught.exception.close()

    async def test_disconnect_releases_execution_slot(self):
        async with connect(self.ws, origin=self.origin) as ws:
            await ws.send(json.dumps({"code": "import time; print('started', flush=True); time.sleep(30)"}))
            while True:
                item = json.loads(await asyncio.wait_for(ws.recv(), timeout=5))
                if "started" in item.get("text", ""):
                    break
        for _ in range(30):
            messages = await self.execute({"code": "print('next run')"})
            if messages[-1]["status"] != "busy":
                self.assertEqual(messages[-1]["status"], "success")
                return
            await asyncio.sleep(0.1)
        self.fail("Disconnect did not release execution slot")
