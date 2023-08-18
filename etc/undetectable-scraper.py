import os, sys

# Add vendor directory to module search path
# parent_dir = os.path.abspath(os.path.dirname(__file__))
# vendor_dir = os.path.join(parent_dir, 'vendor')

# sys.path.append(vendor_dir)
vendors = os.path.join(os.path.dirname(os.path.dirname(__file__)), "libs")
sys.path.append(vendors)

import undetected_chromedriver as uc

driver = uc.Chrome()
print(driver.get("https://google.com"))