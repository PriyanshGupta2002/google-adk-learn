/**
 * Counting Sort Algorithm (for non-negative integers)
 * Time Complexity: O(n + k) where k is the range of key values
 * Space Complexity: O(k)
 */

function countingSort(arr) {
  if (arr.length <= 1) return arr;

  const max = Math.max(...arr);
  const min = Math.min(...arr);

  if (min < 0) {
    throw new Error("Counting sort implementation requires non-negative integers.");
  }

  const count = new Array(max + 1).fill(0);
  const output = new Array(arr.length);

  // Store count of each element
  for (let i = 0; i < arr.length; i++) {
    count[arr[i]]++;
  }

  // Cumulative count
  for (let i = 1; i <= max; i++) {
    count[i] += count[i - 1];
  }

  // Build output array
  for (let i = arr.length - 1; i >= 0; i--) {
    output[count[arr[i]] - 1] = arr[i];
    count[arr[i]]--;
  }

  return output;
}

// Example usage:
const sampleArray = [4, 2, 2, 8, 3, 3, 1];
console.log("Original Array:", sampleArray);
console.log("Sorted Array:", countingSort(sampleArray));

module.exports = countingSort;
