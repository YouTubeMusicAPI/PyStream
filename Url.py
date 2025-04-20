from PyStream import validate_url

url1 = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
url2 = "https://youtu.be/dQw4w9WgXcQ"
url3 = "https://example.com/watch?v=dQw4w9WgXcQ"

print(validate_url(url1))  # Should print True
print(validate_url(url2))  # Should print True
print(validate_url(url3))  # Should print False
