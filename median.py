class Solution:
    def findMedianSortedArrays(self, nums1: list[int], nums2: list[int]) -> float:
        nums = nums1+nums2
        print(nums)
        for i in range(len(nums)):
            for j in range(len(nums)-1):
                if nums[j]> nums[j+1]:
                    nums[j],nums[j+1] =  nums[j+1],nums[j]
        length = len(nums)
        if length %2 !=0:
            return nums[length//2]
        else:
            middle1 = nums[length//2-1]
            middle2 = nums[length//2]
            return (middle1+middle2) /2
Solution = Solution()
print(Solution.findMedianSortedArrays([1,2], [3]))
print(Solution.findMedianSortedArrays([1,2], [3,4]))
