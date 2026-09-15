import urllib.request
import json
import csv

while True:
    print("\n1 - Yeni kullanıcı ara")
    print("2 - Çıkış")
    choice = input("Seçiminiz: ")
    if choice == "1":
        username = input("GitHub kullanıcı adı: ")
        url = f"https://api.github.com/users/{username}/repos"

        req = urllib.request.Request(url)

        data = None
        try:
            with urllib.request.urlopen(req) as response:
                data = response.read().decode()
                info = json.loads(data)

        except urllib.error.HTTPError as e:
            print("HTTP Hatası")
            exit()
        #Ekrana yazdırılan kısım
        print("\n----- GitHub Repositories-----")
        for repo in info:
            print("Name: ", repo['full_name'])
            description = repo['description']

            if description is None:
                description = ("Açıklama bulunmuyor.")
            print("Description: ", description)
            print("URL: ", repo['html_url'])
            print("Language: ", repo['language'])
            print(50 * "-")

        ask = input("Dosyayı kaydetmek istiyor musunuz? (E/H): ")
        try:
            if ask == "E" or ask == "e":
                #Json kayıt kısmı
                filename = f"data/{username}_repositories.json"
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(info, file, indent=4)

                print("JSON dosyası kaydedildi.")


                #CSV kayıt kısmı
                csv_filename = f"data/{username}_repositories.csv"
                with open(csv_filename, "w", newline="", encoding="utf-8") as file:
                    writer = csv.DictWriter(file, fieldnames=["name", "description", "html_url", "language"])
                    writer.writeheader()
                    for repo in info:
                        writer.writerow({
                            "name": repo["full_name"],
                            "description": repo["description"] or "Açıklama bulunmuyor.",
                            "html_url": repo["html_url"],
                            "language": repo["language"]
                        })
                print("CSV dosyası kaydedildi.")

            elif ask == "H" or ask == "h":
                print("Dosya kaydedilmedi.")

        except: 
            print("Dosya kaydedilirken bir hata oluştu.")

    elif choice == "2":
        print("Çıkış yapılıyor...")
        break
    else:
        print("Geçersiz seçim. Lütfen tekrar deneyin.")
    