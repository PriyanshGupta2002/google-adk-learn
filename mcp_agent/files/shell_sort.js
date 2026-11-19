/**
 * Shell Sort Algorithm
 * Time Complexity: O(n log n) to O(n^2) depending on gap sequence
 * Space Complexity: O(1)
 */

function shellSort(arr) {
  const n = arr.length;

  // Start with a large gap, then reduce the gap
  for (let gap = Math.floor(n / 2); gap > 0; gap = Math.floor(gap / 2)) {
    // Do a gapped insertion sort for this gap size
    for (let i = gap; i < n; i++) {
      const temp = arr[i];
      let j;
      for (j = i; j >= gap && arr[j - gap] > temp; j -= gap) {
        arr[j] = arr[j - gap];
      }
      arr[j] = temp;
    }
  }
  return arr;
}

// Example usage:
const sampleArray = [12, 34, 54, 2, 3];
console.log("Original Array:", sampleArray);
console.log("Sorted Array:", shellSort([...sampleArray]));

module.exports = shellSort;
