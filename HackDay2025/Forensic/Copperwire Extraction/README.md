# Forensic

## Copperwire Extraction 
> An intern in cybersecurity at the London police department has discovered that files were exfiltrated from their database. He managed to retrieve the queries used but needs help from someone really skilled in cybersecurity to figure it out!

There is a .pcapng file.
I used wireshark to follow the http/ tcp streams.

[httpstream](../Attachments/Copper/httpstream.png)

There is at least cookie for every stream that looks like base64.

If the "=" at the beginning of every cookie is removed, the base64 can be decoded.

[base64cookie](../Attachments/Copper/base64cookie.png)

The first cookie contains the first data of an image file, my guess is that each cookie concatenated will form an image.
Time to exfiltrate every cookie then.

`tshark -r capture.pcap -Y "http.cookie" -T fields -e http.cookie > cookies.txt`

    import base64
    
    with open('cookies.txt', 'r') as file:
        cookies = file.readlines()
    
    # Decode Base64 cookies (after removing the first character) and concatenate
    image_data = b""
    for cookie in cookies:
        cookie = cookie.strip() 
        if cookie:
            try:
                cleaned_cookie = cookie[1:] 
                decoded = base64.b64decode(cleaned_cookie)
                image_data += decoded
            except Exception as e:
                print(f"Failed to decode cookie: {cookie} - Error: {e}")
    
    # Save to an image file
    with open('output_image.jpg', 'wb') as img_file:
        img_file.write(image_data)
    
    print("Image reconstructed and saved as output_image.jpg")

This is the output :

[1D](../Attachments/Copper/1D.png)

The "1" hints that there are more images. But where are they ?  
I used foremost to check the image and extract files.

[moreimages](../Attachments/Copper/moreimages.png)

The images have a letter and a number indicating their position.

[allimages](../Attachments/Copper/allimages.png)

The flag can then be easily reconstructed.

`HACKDAY{D4t4_Exf1Ltr@t10n}`
