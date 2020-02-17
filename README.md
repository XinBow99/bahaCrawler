# Baha_Crawler

Baha_Crawler is a Crawler for restructure forum.gamer.com.tw information.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary modules.

```bash
pip install requests
pip install pandas
pip install openpyxl
```

## Usage
Change the following of hashtag

```python
self.keyWordList = ['星爆','發財'] #Search words
self.bsn = "60076" #Baha board id,60076 is 場外休憩區
self.download = True #Download the post pictures
self.pageDelay = 0   #Crawler page delay
self.innerDelay = 0  #Crawler post delay
```

## Download picture
save path is ./bahaImage/[searchWord]/[postTitle]
## Excel and output
#json: ./[searchWord].json
#xlsx: ./[searchWord].xlsx
