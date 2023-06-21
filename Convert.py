import re

# Read index.html file
with open('index.html', 'r') as file:
    index_content = file.read()

# Extract video title and data-src from index.html
match = re.search(r'<p>(.*?)</p>', index_content)
video_title = match.group(1)

data_src_match = re.search(r'data-src="(.*?)"', index_content)
data_src = data_src_match.group(1)

# Read test.html file
with open('test.html', 'r') as file:
    test_content = file.read()

# Replace video title and data-src in test.html
test_content = re.sub(r'<p id="video-title".*?</p>', f'<p id="video-title" data-src="{data_src}">{video_title}</p>', test_content)

# Write updated content to test.html
with open('test.html', 'w') as file:
    file.write(test_content)

print("Conversion completed successfully!")
