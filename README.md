# Job-Oriented-Concurrency
A python library for concurrency based on jobs and dependencies between them.

# How to use
To use the library/framework you first have to initalize an object of the type JocTree. 
To add a job/function to the tree use the method [JocTree].add_func([function])
To add a dependency to the tree between two functions use the method [JocTree].add_connect([parent function], [child function])
to add a start function, or a function that will be called when the tree runs use the method [JocTree].add_start_func([function])
to add an end function, or the function that the tree will use as the return value use the method [JocTree].add_end_func([function])
note: there can only be one end function and calling add_end_func again will change the end function. It will not delete the other function or the connections it has.
to delete anything just change the add in the method signature to del. 
note: to delete a function from the tree it must have no connections. The tree will raise a value error.
to run the tree use the method [JocTree].run()