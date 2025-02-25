```python
from ocr_toolkits import synthetic_khmerid

synthetic_khmerid(
    size=100,
    size=(1575, 1024), # size of images 
    profile_path="images", # Path of user profile
    label="line-level", "segment-level", "None", # Default "None"
    save_json=True # default False
    output_path="synth_khmerid" # which should have images dir, labels dir, classes.txt
)

```


- line-level : 
1. id_number
2. khm_name
3. eng_name
4. dob
5. pob
6. address_1
7. address_2
8. issue_expiry_date
9. identity
10. mrz1
11. mrz2
12. mrz3

- segment-level : 
1. id_number
2. pre-khm-name
3. khm-fname
4. khm-lname
5. eng-fname
6. eng-lname
7. pre-dob
8. dob
9. pre-gender
10. gender
11. pre-height
12. height
13. pre-pob
14. pob
15. pre-address
16. address1
17. address2
18. pre-issue-expiry-date
19. expiry-date
20. pre-identity
21. identity
22. mrz1
23. mrz2
24. mrz3
25. photo
26. signature