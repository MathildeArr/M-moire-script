from bs4 import BeautifulSoup
import json
import re
import sys
import time

# Remove the full #
def removeFullHashtag(input_string):
    result = re.sub(r'#\w+\s*', '', input_string)
    return result

# Remove the # only
def removeHashtag(input_string):
    return input_string.replace("#","")

# Remove the full @
def removeFullAt(input_string):
    result = re.sub(r'@\w+\s*', '', input_string)
    return result

# Remove the @ only
def removeAt(input_string):
    return input_string.replace("@","")

# Does not work very well
def removeURL(input_string):
    # Define a regular expression to match URLs starting with http or https
    result = re.sub(r'^https?:\/\/.*[\r\n]*', '', input_string, flags=re.MULTILINE)
    return result

def parse(html_file_path):

    # Read the full HTML file
    with open(html_file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Initialize the parser
    soup = BeautifulSoup(html_content, 'html.parser')

    # Number of posts
    n_post = 1

    # Dict that contains all the posts and related informations
    data_dict = {}

    # Get the main post div (username, post, likes, etc.)
    maindiv = soup.find_all('div', class_='css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu')

    for maindivsub in maindiv:

        # Get info about the post (likes, reposts, etc)
        full_info = maindivsub.find_all('span', class_='css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0')
        
        # Get the full post
        post_content_div = maindivsub.find_all('div', class_='css-901oao css-cens5h r-18jsvk2 r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0')
        
        # Iterate through the <div> elements and extract text from <span> elements
        for div_element in post_content_div:

            # Find all the text in spans in the div
            span_elements = div_element.find_all("span")

            # Extract and print the text of the found <span> elements
            full_post = ""
            for span_element in span_elements:
                # Remove some chars and/or words
                purged = removeFullHashtag(span_element.text)
                purged = removeAt(purged)
                #purged = removeURL(purged)
                full_post +=  purged.replace("\n","")

            # Create a dict from extracted HTML content
            data_dict[n_post] = {
                "name": full_info[0].text,
                "username": full_info[1].text,
                "content": full_post,
                "nb_like": full_info[-2].text,
                "nb_repost": full_info[-3].text,
                "nb_comment": full_info[-4].text,
                "nb_view": full_info[-1].text
            }
            # Increment the number of posts
            n_post += 1

    # Converts the dict to JSON and remove all unicode chars
    json_data = json.dumps(data_dict, indent=2, ensure_ascii=False).encode('utf8')
    # Print the JSON
    print(json_data.decode())
    # Create json file and write content
    output_file = open("output_file.json", "w")
    output_file.write(json_data.decode())

# If argument then run script, if not print usage
if __name__ == "__main__":

    print("Extract all posts from HTML page, apply some filters and convert it to JSON. \n")

    if len(sys.argv) < 2:
        print("[X] Usage : python script_name.py name_of_html_file_to_parse")
        exit()

    print(f"Parsing {sys.argv[1]} \n")
    time.sleep(1)
    parse(sys.argv[1])