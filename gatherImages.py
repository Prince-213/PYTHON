from simple_image_download import simple_image_download as simp

response = simp.simple_image_download

keywords = [ "Person", "chair", "table", "door", "person in office", "chair in office", "table in office", "door in office" ]

for kw in keywords:
    response().download(kw, 60)