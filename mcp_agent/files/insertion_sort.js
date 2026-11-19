/**
 * Insertion Sort Algorithm
 * Time Complexity: O(n^2) Worst/Average, O(n) Best
 * Space Complexity: O(1)
 */

function insertionSort(arr) {
  const len = arr.length;

  for (let i = 1; i < len; i++) {
    const key = arr[i];
    let j = i - 1;

    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }
    arr[j + 1] = key;
  }
  return arr;
}

// Example usage:
const sampleArray = [12, 11, 13, 5, 6];
console.log("Original Array:", sampleArray);
console.log("Sorted Array:", insertionSort([...sampleArray]));

module.exports = insertionSort;
