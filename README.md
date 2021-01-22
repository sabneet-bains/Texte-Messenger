# Texte - Instant Messenger

Texte is a Python-based Qt graphical instant messaging program utilizing the QUdpSocket for semi-secure peer-to-peer communications. 

![](https://github.com/sabneet95/Texte-Messenger/blob/master/messaging.png)

→ `To compare, the program reads a user-provided directory with input files of four sizes: 50, 1000, 2000, 5000 and 10000 integers, and three versions including random, reverse, and normal.`

## Requirements

[Python 3.9.1 (64-bit) or above](https://www.python.org/downloads/)
[PyQt5](https://www.riverbankcomputing.com/software/pyqt/download)

## Build Tested

IntelliJ IDEA 2020.3 RC (Community Edition)
* Build #IC-203.5981.114, built on November 10, 2020
* Runtime version: 11.0.9+11-b1145.21 amd64
* VM: OpenJDK 64-Bit Server VM by JetBrains s.r.o.
* Windows 10 10.0
* GC: ParNew, ConcurrentMarkSweep
* Memory: 1981M
* Cores: 8

## Usage

1)	Open the project in **IntelliJ IDEA** > _build_ & run the driver class.


```java
public class driver {
    @SuppressWarnings("InstantiationOfUtilityClass")
    // If the user provides faulty input, an IOException takes care of bad I/O
    public static void main(String[] args) throws IOException {

    ...
        ...
            ...

            // Executes the read_input function and subsequent logic
            new read_input(input_file, output_file);
```

2)	Either provide the input directory as command-line arguments when executing the driver class or later when the 
      conditional logic prompts **<!>**

```
    >>  java driver

        <!> Oops, you didn't provide the required input directory! <!>

        No worries, go ahead and type the input file directory: █
```

3)	According to the lab specifications, the program uses linked association and recursion to sort and 
      list a total number of comparisons and exchanges for the respective sorting algorithm.

```java
public void write_output(int[] array, String input_file, int low, int high, int type, int file_number) throws IOException {

        final_sort(array, low, high, type);
```

4)	For added convenience, pre-run output files _"quick_sort_results.csv"_ and _"natural_merge_sort_results.csv"_ are provided
      based on the original lab and student-generated inputs.


## Contributing

Independent academic work, with additional references from 

https://www.geeksforgeeks.org/quick-sort/

https://www.geeksforgeeks.org/insertion-sort/

https://www.geeksforgeeks.org/merge-sort-for-linked-list/


## License
[MIT](https://choosealicense.com/licenses/mit/)
