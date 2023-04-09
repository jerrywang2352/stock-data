
## Challenge Description
We are seeking approaches to _pooling_ mortgage loans (hereafter referred to simply as "loans").  We recommend an approach
based on "knapsack alrogithms", a family of algorithms that attempt to 
maximize the value of _items_ placed in a _container_ (AKA a _knapsack_) without exceeding the container's
_capacity_.  
In our subject area, the container/knapsack is called a _pool_, and the items to be
placed into those pools are _loans_.  
Your challenge:  given approximately 1.4 million loans, try to place as many of them as possible
into pools.  There are ten _classes_ of pools, each of which has a specific
_value_ and a set on constraints that determine which loans can be placed into the pool.  You can make multiple instances of each pool class; however,
**please remember that a given loan can appear in at most one pool**.  Your base score will be 
the total values of all of the pools that you successfully construct.  On top of this base 
score, you will receive bonus points for completeness of your solution, innovation, and throughput/efficiency.

## Loans
Mortgage loans are the input dataset for this challenge.  For the purposes of this challenge,
we have supplied you with a set of about 1.5 million loan records.  There are twelve attributes per
loan:

| Attribute       | Type   | Description                                   
|-----------------|--------|-----------------------------------------------|
| loan_id         | string | The loan's unique identifier                  |
| upb             | float  | The loan's unpaid principal balance           |
| note_rate       | float  | The loan's note rate, AKA its interest rate   
| borrower_fico   | int    | The primary borrower's credit (FICO) score
| coborrower_fico | int    | The coborrower's credit (FICO) score -- only present if more than one borrower
| combined_fico   | int    | If both borrower_fico and coborrower_fico are non-null then this is the average of those two values, else it is equal to borrower_fico
| state           | string | The two-letter state code where the property is located
| dti             | int    | debt-to-income ratio of the borrower
| ltv             | int    | loan-to-value ratio -- ratio of the amount of the loan to the price of the home
| maturity_date   | string | (form is mmyyyy) the month and year in which the loan matures, AKA, when the balance is scheduled to reach zero
| loan_term       | int    | The duration of the loan, expressed as months
| property_type   | string | Two-letter code indicating the type of dwelling (SF for single family, CO for condo, etc.)

### Input Files
The input dataset is comprised of 16 files in the GitHub repo, fnma-dataset-00.txt 
throught fnma-dataset-15.txt.  You should clone the repo and then concatenate the files
to create a single input file.  The fnma-dataset-00.txt file has a header row,
so make sure that is the file that is at the top of the concatenated file.

## Pools

Your challenge is to build as many _pools_ of loans as you can from the 
loan dataset, and to maximize the _value_ of each of the pools that 
you build.
There are ten _classes_ of pools.  Each pool class has a capacity, which is the maximum total UPBs of the loans placed into the pool.
Each pool also has a set of _constraints_.  These constraints are the rules that define the 
loans that are allowed to be added to the pool; for example, a pool might only allow loans where 
the DTI (debt-to-income ratio) is between 28 and 42.  There are _overall constraints_ that
apply to all pool classes, and there are _specific_ constraints for each class.
### Overall Constraints
- Maturity Date -- all loans within a pool must have the same maturity_date
- Loan Term -- all loans within a pool must have the same loan_term
- FICO -- if combined_fico is not null, then it must be used for all calculations involving FICO scores
- Property Type -- **optional bonus constraint** -- for each pool that restricts its loans to all have the same property_type value, for example if they are all loans for condos ('CO'), then you will receive bonus points for adhering to this optional constraint.
- **Most Important Of All** -- A loan can be in at most **one** pool
### Pool Classes and Constraints
There are ten pool classes.  Each class has a set of constraints that determine which
loans are eligible to be placed into pools of that class.  There are six of these _specific_ constraints per class:

|Constraint     | Description    |
|---------------|----------------|
|Pool Size      |The min and max size of the pool, where size is defined as the sum of the UPBs of the loans in the pool
|Note Rate      |The min and max loan note_rate value allowed in the pool
|FICO Score     |The min and max combined_fico value allowed in the pool
|State %        |The maximum percentage of loans from any given US state allowed into the pool; for example, if the value is 5%, then the total number of loans from a single state, such as NY, cannot exceed 5% of the loans in the pool
|DTI            |The min and max dti value allowed in the pool
|LTV            |The min and max ltv value allowed in the pool

As previously mentioned, there are ten pool classes, each of which has preset values for the six
specific constraints described above:


| Class  |Size |Note Rate|FICO|State %|DTI|LTV|
|--------|-----|---------|----|-------|---|---|
| 1      |$5,000,000 - $20,000,000|5.00 - 7.00|640 - 745|5%|35 - 50|75-85|
| 2      |$5,000,000 - $20,000,000|4 - 6|600 - 770|5%|40 - 45|70 - 90|
| 3      |$5,000,000 - $20,000,000|3 - 7|600 - 700|10%|45 - 55|60 - 95|
| 4      |$5,000,000 - $20,000,000|3 - 7|670 - 750|5%|47 - 52|35 - 80|
| 5      |$5,000,000 - $20,000,000|3 - 7|675 - 780|5%|30 - 55|60 - 85|
| 6      |$5,000,000 - $30,000,000|3 - 7|690 - 790|15%|15 - 35|70 - 85|
| 7      |$5,000,000 - $30,000,000|2 - 5|720 - 850|5%|10 - 45|70 - 80|
| 8      |$15,000,000 - $40,000,000|1.5 - 7|550 - 740|5%|20 - 45|0 - 85|
| 9      |$15,000,000 - $40,000,000|1.5 - 9|730 - 770|5%|35 - 45|90 - 95|
|10      |$15,000,000 - $40,000,000|1.5 - 6.5|400 - 850|25%|20 - 60|70 - 99|


# Pool Value

Every pool class has an associated value, or score.  Class 1 has the highest
score, and they descend from there to class 10, which has the lowest score.
Your implementation will be evaluated partially on the sum of the scores
of the pools that you construct, so you want to optimize your algorithm to favor
the construction of lower-numbered pool classes (1, 2, 3) over the construction
of higher-numbered pool classes.  

# Output Format
In order for us to evaluate your implementation, we need the output to
be in a specific format.

# Output File Name Format
Your output should consist of one text file per pool that you generate.  The 
file name should be of the form pool-<class>-<pool-num>.txt; for example,
if you generate two class-three pools and 1 class-four pool, then the file names would be:

- pool-3-1.txt
- pool-3-2.txt
- pool-4-1.txt

## Output Row Format
Each pool file should contain one loan per line.  Each line should contain
all of the loan's input attributes/columns, delimited by pipes.

# Utilize Our Mentors
We have a group of mentors who are competent programmers and are knowledgeable in the 
mortgage subject domain.  Do not hesitate to reach out to us at our table or via Slack.





 
