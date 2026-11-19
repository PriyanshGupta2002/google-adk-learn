/**
 * Bubble Sort Algorithm
 * Time Complexity: O(n^2) Average/Worst, O(n) Best
 * Space Complexity: O(1)
 */

function bubbleSort(arr) {
  const len = arr.length;
  let swapped;

  for (let i = 0; i < len; i++) {
    swapped = false;
    for (let j = 0; j < len - 1 - i; j++) {
      if (arr[j] > arr[j + 1]) {
        [arr[j], arr[j + 1]] = [arr[j + 1], arr[j]];
        swapped = true;
      }
    }
    // If no elements were swapped, array is already sorted
    if (!swapped) break;
  }
  return arr;
}

// Example usage:
const sampleArray = [64, 34, 25, 12, 22, 11, 90];
console.log("Original Array:", sampleArray);
console.log("Sorted Array:", bubbleSort([...sampleArray]));

module.exports = bubbleSort;
