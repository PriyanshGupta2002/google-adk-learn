/**
 * Selection Sort Algorithm
 * Time Complexity: O(n^2)
 * Space Complexity: O(1)
 */

function selectionSort(arr) {
  const len = arr.length;

  for (let i = 0; i < len - 1; i++) {
    let minIndex = i;
    for (let j = i + 1; j < len; j++) {
      if (arr[j] < arr[minIndex]) {
        minIndex = j;
      }
    }
    if (minIndex !== i) {
      [arr[i], arr[minIndex]] = [arr[minIndex], arr[i]];
    }
  }
  return arr;
}

// Example usage:
const sampleArray = [64, 25, 12, 22, 11];
console.log("Original Array:", sampleArray);
console.log("Sorted Array:", selectionSort([...sampleArray]));

module.exports = selectionSort;
