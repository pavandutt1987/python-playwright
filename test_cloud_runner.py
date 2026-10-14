import asyncio
import unittest
import uuid

from app import runner


class RunnerTests(unittest.IsolatedAsyncioTestCase):
    async def run_code(self, code, language="python", timeout=10):
        return [item async for item in runner.execute_code_stream(
            uuid.uuid4().hex, language, code, timeout_sec=timeout
        )]

    async def test_python_output_and_cleanup(self):
        items = await self.run_code("print('cloud runner ready')")
        self.assertEqual(items[-1]["status"], "success")
        self.assertIn("cloud runner ready", items[-1]["full_output"])
        self.assertFalse(runner.ACTIVE_PROCESSES)
        self.assertFalse(runner.RESERVED_RUNS)

    async def test_silent_script_times_out(self):
        items = await self.run_code("import time; time.sleep(30)", timeout=0.5)
        self.assertEqual(items[-1]["status"], "timeout")
        self.assertFalse(runner.ACTIVE_PROCESSES)

    async def test_output_without_newlines_is_bounded(self):
        items = await self.run_code("import sys; sys.stdout.write('x' * 2000000)")
        self.assertEqual(items[-1]["status"], "output_limit")
        self.assertLess(len(items[-1]["full_output"]), runner.MAX_OUTPUT_BYTES + 100)

    async def test_busy_run_is_rejected(self):
        runner.RESERVED_RUNS.update(f"occupied-{i}" for i in range(runner.MAX_RUNS))
        try:
            items = await self.run_code("print('should not run')")
            self.assertEqual(items[-1]["status"], "busy")
        finally:
            runner.RESERVED_RUNS.clear()

    async def test_cancel_releases_slot_and_process(self):
        async def consume():
            return await self.run_code("import time; time.sleep(30)")
        task = asyncio.create_task(consume())
        for _ in range(200):
            if runner.ACTIVE_PROCESSES:
                break
            await asyncio.sleep(0.01)
        self.assertTrue(runner.ACTIVE_PROCESSES)
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertFalse(runner.ACTIVE_PROCESSES)
        self.assertFalse(runner.RESERVED_RUNS)

    async def test_javascript_and_typescript(self):
        for language, code in [
            ("javascript", "const { chromium } = require('playwright'); console.log(chromium.name());"),
            ("typescript", "import { chromium } from 'playwright'; console.log(chromium.name());"),
        ]:
            with self.subTest(language=language):
                items = await self.run_code(code, language)
                self.assertEqual(items[-1]["status"], "success", items[-1])
                self.assertIn("chromium", items[-1]["full_output"])

    async def test_playwright_test_runner(self):
        items = await self.run_code(
            "import { test, expect } from '@playwright/test'; "
            "test('cloud smoke', async () => { expect(2 + 2).toBe(4); });",
            "typescript",
        )
        self.assertEqual(items[-1]["status"], "success", items[-1])


if __name__ == "__main__":
    unittest.main()
