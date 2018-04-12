
// File: FCIII_HW3_2.cpp
// Authors:

#include <iostream>
#include <vector>
#include <algorithm>     // for minmax_element()
#include <random>        // for random number engines and distributions
#include <ctime>         // for time()
#include <iomanip>       // for setw()
using namespace std;

// Mersenne Twister random number engine
mt19937 mte;

// selection sort
void selection_sort(vector<int>& v)
{
   int k(0);         // next slot for sorted value
   for ( ; k < v.size(); ++k) {
      int low_i(k);  // index of lowest remaining value
      for (int j(k); j < v.size(); ++j) {  // nested! O(N^2)
         if (v[j] < v[low_i])
            low_i = j;
      }
      // now, swap the lowest remaining value into slot k
      int temp(v[k]);
      v[k] = v[low_i];
      v[low_i] = temp;
   }
}

// insertion sort
void insertion_sort(vector<int>& v)
{
   int k(1);           // next step
   for ( ; k < v.size(); ++k) {
      int temp(v[k]);
      int j(k-1);      // highest index of sorted portion
      for ( ; j >= 0 && v[j] > temp; --j) { // nest! O(N^2)
         v[j+1] = v[j];  // shift v[j-1] to v[j]
      }
      // now, put temp into correct slot
      v[j+1] = temp;
   }
}

// bubble sort
void bubble_sort(vector<int>& v)
{
   for (int k(0); k < v.size(); ++k) {        // iteration
      for (int j(0); j < v.size()-1; ++j) {   // nest! O(N^2)
         if (v[j] > v[j+1]) {
            int temp(v[j]);
            v[j] = v[j+1];
            v[j+1] = temp;
         }
      }
   }
}

// "optimized" bubble sort
void bubble_sort_op(vector<int>& v)
{
   for (int k(0); k < v.size(); ++k) {    // iteration
      size_t up_limit = v.size()-k-1;     // 1st optimization
      size_t nswaps(0);                   // 2nd optimization
      for (int j(0); j < up_limit; ++j) { // nest! O(N^2)
         if (v[j] > v[j+1]) {
            nswaps += 1;
            int temp(v[j]);
            v[j] = v[j+1];
            v[j+1] = temp;
         }
      }
      if (nswaps == 0)  // sorted -- we are DONE!
         return;
   }
}

// quicksort components
int partition(int a[], int size)
{
    if (size <= 0) return -1;    // empty array
    uniform_int_distribution<int> iunif(0,size - 1);
    swap(a[0], a[iunif(mte)]);  // to optimize
    int pivot(a[0]);
    int j(0);    // index for <= pivot
    int k(1);    // index for > pivot OR untested
    for ( ; k < size; ++k)       // test each array element
        if (a[k] <= pivot)       // ... against the pivot
            swap(a[++j], a[k]);  // call by reference
    swap(a[0], a[j]);            // pivot is in correct place!
    return j;
}

void quicksort_array_help(int a[], int size)
{
    if (size == 0) return;           // empty array
    int p_index = partition(a, size);
    if (p_index >= 0) {
       quicksort_array_help(a, p_index);
       quicksort_array_help(a + p_index + 1,
                                 size - p_index - 1);
    }
}

void quicksort(vector<int>& vi)
{
    // treat vector<int> as array-of-size int
    quicksort_array_help(&vi[0], vi.size());

}

// merge sort
void merge_sort(vector<int>& vi)
{
    if (vi.size() <= 1) return;  // nothing to do!

    // split vi into a front half and a back half
    vector<int> vft(&vi[0], &vi[0]+vi.size()/2);
    vector<int> vbk(&vi[0]+vi.size()/2, &vi[0]+vi.size());

    merge_sort(vft);     // sort the front half
    merge_sort(vbk);     // sort the back half

    // merge the sorted front and back into vi
    // notice that vi.size() == vft.size() + vbk.size()
    int ift(0), ibk(0);  // front, back half indexes
    for (int i(0); i < vi.size(); ++i) {  // vi index
        // if front is used up, get the back value
        if (ift >= vft.size()) vi[i] = vbk[ibk++];
        // else if back is used up, get the front value
        else if (ibk >= vbk.size()) vi[i] = vft[ift++];
        // else, get the lesser of the front and back values
        else vi[i] = vft[ift] < vbk[ibk]
                      ? vft[ift++] : vbk[ibk++];
    }
}

void counting_sort(vector<int>& vi)
{
    if (vi.size() <= 1) return;   // nothing to do!

    auto mn_mx = minmax_element(vi.begin(), vi.end());
    int min = *mn_mx.first;       // min value
    int max = *mn_mx.second;      // max value
    int M = max - min + 1;        // count vector size

    vector<int> counts(M);        // vector of M 0s
    for (int i(0); i < vi.size(); ++i)
        counts[vi[i] - min] += 1; // increment value counts

    int k(0);        // subscript in vi
    for (int i(0); i < counts.size(); ++i) {
        // there are counts[i] occurrences of i + Min
        // in vector vi
        for (int j(0); j < counts[i]; ++j) {
            vi[k++] = i + min;  // post-increment subscript k
        }
    }
}


int main()
{

	// sort algorithm timing tests
	cout << "\nTIMING TESTS:\n\n";

	uniform_int_distribution<int> iunif(1, 2048);

// void (*)(vector<int>&) means pointer-to function taking a reference-to-vector<int> argument
//                              and returning void
// the name of a function is the address of the function, in an analogous way to the name
// of an array being the address of the initial element in the array
//
// sort_algos is a vector of pairs, where the first element of the pair is a string (the name
// of the sort algorithm) and the second element is the address of the sort function
//
	vector<pair<string,void (*)(vector<int>&)>> sort_algos{
			{ "selection_sort", selection_sort },
			{ "insertion_sort", insertion_sort },
			{ "bubble_sort", bubble_sort },
			{ "bubble_sort_op", bubble_sort_op },
			{ "quicksort", quicksort },
			{ "merge_sort", merge_sort },
			{ "counting_sort", counting_sort } };

	for (int n_values = 1'000; n_values <= 128'000; n_values *= 2) {
		vector<int> vi_test;
		for (int i(0); i < n_values; ++i)
			vi_test.push_back(iunif(mte));
		vector<int> vi_test_copy(vi_test);
		sort(vi_test_copy.begin(), vi_test_copy.end());    // use standard sort algorithm

		for (int j(0); j < sort_algos.size(); ++j) {
			vector<int> via_test(vi_test);
			time_t astart = time(0);
			(*sort_algos[j].second)(via_test); // call the pointed-to algorithm
			time_t astop = time(0);
			if (via_test != vi_test_copy) {    // yikes!  the current sort algorithm did not work!
				cout << "sort failed!\n";
			}
			cout << setw(20) << sort_algos[j].first << " of "
			     << setw(10) << n_values
			     << " values took " << (astop - astart) << " seconds\n";
		}
		cout << '\n';
	}

}

