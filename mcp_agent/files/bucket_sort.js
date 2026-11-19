/**
 * Bucket Sort Algorithm
 * Time Complexity: O(n + k) Average, O(n^2) Worst
 * Space Complexity: O(n)
 */

function bucketSort(arr, bucketSize = 5) {
  if (arr.length <= 1) return arr;

  let min = arr[0];
  let max = arr[0];

  for (let i = 1; i < arr.length; i++) {
    if (arr[i] < min) min = arr[i];
    else if (arr[i] > max) max = arr[i];
  }

  const bucketCount = Math.floor((max - min) / bucketSize) + 1;
  const buckets = Array.from({ length: bucketCount }, () => []);

  for (let i = 0; i < arr.length; i++) {
    const bucketIndex = Math.floor((arr[i] - min) / bucketSize);
    buckets[bucketIndex].push(arr[i]);
  }

  const sortedArray = [];
  for (let i = 0; i < buckets.length; i++) {
    // Simple insertion sort on individual buckets
    insertionSort(buckets[i]);
    sortedArray.push(...buckets[i]);
  }

  return sortedArray;
}

function insertionSort(arr) {
  for (let i = 1; i < arr.length; i++) {
    const key = arr[i];
    let j = i - 1;
    while (j >= 0 && arr[j] > key) {
      arr[j + 1] = arr[j];
      j--;
    }
    arr[j + 1] = key;
  }
}

// Example usage:
const sampleArray = [0.42, 0.32, 0.33, 0.52, 0.37, 0.47, 0.51];
console.log("Original Array:", sampleArray);
console.log("Sorted Array:", bucketSort(sampleArray, 0.1));

module.exports = bucketSort;
