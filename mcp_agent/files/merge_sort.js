/**
 * Merge Sort Algorithm
 * Time Complexity: O(n log n)
 * Space Complexity: O(n)
 */

function mergeSort(arr) {
  if (arr.length <= 1) return arr;

  const mid = Math.floor(arr.length / 2);
  const left = mergeSort(arr.slice(0, mid));
  const right = mergeSort(arr.slice(mid));

  return merge(left, right);
}

function merge(left, right) {
  const result = [];
  let leftIndex = 0;
  let rightIndex = 0;

  while (leftIndex < left.length && rightIndex < right.length) {
    if (left[leftIndex] < right[rightIndex]) {
      result.push(left[leftIndex]);
      leftIndex++;
    } else {
      result.push(right[rightIndex]);
      rightIndex++;
    }
  }

  return result
    .concat(left.slice(leftIndex))
    .concat(right.slice(rightIndex));
}

// Example usage:
const sampleArray = [38, 27, 43, 3, 9, 82, 10];
console.log("Original Array:", sampleArray);
console.log("Sorted Array:", mergeSort(sampleArray));

module.exports = mergeSort;
