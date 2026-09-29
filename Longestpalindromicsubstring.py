class Solution:
     def longestPalindrome(self, s: str) -> str:
          result = ""
          for i in range(len(s)):
               for j in range(i,len(s)):
                    substring = s[i:j+1]
                    if len(substring)>1:
                        if substring == substring[::-1]:
                                 return substring

                        

Solution = Solution()
print(Solution.longestPalindrome("babad"))
               
                    