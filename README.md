# Dashboard-py
Interactive covid Dashboard that displays different graphs based on the user's selection . 
## Getting started
Make sure you have the package manager [pip](https://pip.pypa.io/en/stable/)
### Running the app
first clone the repository and open the directory location in your terminal.<br />
To clone using https use 
```bash
git clone https://github.com/Heatdh/Dashboard-py.git
```
Create and activate a new virtual environment (not necessary but recommended):
This can differs for each machine (try adding py -m in case this command doesn't work)<br />
On Windows
```bash
py -m venv <name_of_virtualenv>
//activate it 
<name_of_virtualenv>\Scripts\activate.bat

```
on linux
```bash
python3 -m venv <name_of_virtualenv>
source <name_of_virtualenv>/bin/activate

``` 
Install the requirements:
```bash
pip install -r requirements.txt
``` 
Run the app:
```bash
python main.py
``` 
open the provided address on your browser
### Note 
The original datas were provided by [RKI](https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Daten/Impfquotenmonitoring.html;jsessionid=4D8099EBA62B4252533BA42EDB0CA18D.internet092?nn=13490888)  as an xlsx file  and these were cleaned and the sheets were divied and converted into csv using :

```python
import pandas as pd 

data_xls = pd.read_excel(<Path>>, dtype=str, index_col=None)
data_xls.to_csv('<Path + csv extension >', encoding='utf-8', index=False)
```
## License and copyright 
© Technical Universtiy Of Munich -- Python for Engineering Data Analysis - from Machine Learning to Visualization

