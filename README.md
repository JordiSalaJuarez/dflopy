# DRAFT
## dflopy

dflopy is a data flow analyzer for python, doing analyzes like inter
procedural analysis, call graphs, ...

### Implementation

Doing a data flow engine from scratch is quite a hassle, thus we are
basing our analyses on top of a datalog representation. This means
cleaner abstractions and we are leaving the tought work to some 
higly optimized datalog engine like souffle or mangle

## Requirements
- Python 3.10 or higher
- Soufflé (Logic Defined Static Analysis)

## Usage
```bash
# Generate datalog code
>> python3 main.py > my_code.dl
# Run the Datalog solver
>> souffle my_code.dl
>> echo -e 'func\treaches\n' && cat callGraph.csv
func    reaches

main    foo
main    bar
main    baz
foo     bar
foo     baz
bar     baz
```
