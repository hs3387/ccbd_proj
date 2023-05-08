<div align="center">

<samp>

<h1> COMS 6995: Project - Cloud Computing Project</h1>

<h3> Hayagreevan Sriram: hs3387 <br>  Adithya Krishnakumar Krishna: akk2188 <br> Vignay Chanda: vc2608 <br> Shamin Aggarwal: sa4129</h3>
</samp>   

</div>     

## Fashion Recommender
The proliferation of online shopping platforms has made it easier for consumers to shop from the comfort of their homes or on the go, and swiftly too! But the sheer volume of products available can be overwhelming. Traditional keyword-based text searches can often return irrelevant or inaccurate results, making it difficult for users to find clothing items that match their preferences. This proposal presents a novel approach that uses image recognition and pattern matching to revolutionize the online shopping experience, providing users with a more convenient and efficient way to find clothing items they like.


## Directory setup
<!---------------------------------------------------------------------------------------------------------------->
The structure of the repository is as follows: 

- `__pycache__`: Library Files for Python Implementations
- `frontend`: 
	- `fashionRecommender-swagger.yaml` : Contains the basic API endpoints planned to be implemented
- `img`: Suggestions ML Model I/O sample
- `proto`: Original Frontend Prototype
- `src`: Backend Source Code
	- `__pycache__`: Py Libraries
	- `clothing_identify`:
		- `label2suggestion.py`: Suggestions generator script part 1
		- `product_suggestions.py`: Suggestions generator script part 2
		- `driver.py`: Main Driver script that compiles the functionality of all modules
		- `Fashion Recommendation Table.xlsx`: Tables of reccomendation combinations 
	- `clothing_login.py`: Sign up and Authentication handler script
	- `clothing_getter.py`: GET call handler for frontend, to return required data
	 `label2suggestion_2.0.ipynb`: ML Model to generate clothing recommendation pairs
- `tests`: Test Scripts and Pages used to test component Functionalities
- `utils`: ML model utility and library files

---

## Dependencies
- Python 3.10
- HTML
- CSS
- JavaScript
- YAML
- AWS CLI
- 