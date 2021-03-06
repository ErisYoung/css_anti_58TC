import re
import base64
import requests as rq
from copyheaders import headers_raw_to_dict
from fontTools.ttLib import TTFont
from lxml import etree
import  lxml.html as H


headers=b"""
accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9
cache-control: max-age=0
cookie: f=n; commontopbar_new_city_info=5%7C%E8%8B%8F%E5%B7%9E%7Csu; commontopbar_ipcity=hz%7C%E6%9D%AD%E5%B7%9E%7C0; id58=c5/nn1xe7U4ywTecgnC7Ag==; 58tj_uuid=9f7077b1-1975-463b-85ac-9527b4a4ac3f; sessionid=6857625c-ff00-47aa-b1e2-2fc07112d5ab; param8616=0; param8716kop=1; JSESSIONID=AFADDF58F973FB4989A495AC949578A8; new_uv=2; utm_source=; spm=; init_refer=; jl_list_left_banner=1; als=0; Hm_lvt_a3013634de7e7a5d307653e15a0584cf=1554791615; Hm_lpvt_a3013634de7e7a5d307653e15a0584cf=1554791615; wmda_uuid=141ea88c5ba3413bc1a20a28f391118a; wmda_new_uuid=1; wmda_session_id_1731916484865=1554791616012-0246c2d1-6521-4700; wmda_visited_projects=%3B1731916484865; f=n; new_session=0; ppStore_fingerprint=CA099D7310246607A7B358E3962CB00581402866AC956EC4%EF%BC%BF1554791718315
user-agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
"""

headers=headers_raw_to_dict(headers)

def generate_font_file(path="test.ttf"):
    a=b"d09GRgABAAAAABskAAsAAAAAJlgAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAABHU1VCAAABCAAAADMAAABCsP6z7U9TLzIAAAE8AAAARAAAAFZtBmZoY21hcAAAAYAAAAHzAAAFThOUhbpnbHlmAAADdAAAFEMAABl0ai65rmhlYWQAABe4AAAALwAAADYYxE1/aGhlYQAAF+gAAAAcAAAAJBFsBhhobXR4AAAYBAAAADAAAAC8RisAAGxvY2EAABg0AAAAYAAAAGCQCpaObWF4cAAAGJQAAAAfAAAAIAFCAGFuYW1lAAAYtAAAAXIAAALQd5CEoXBvc3QAABooAAAA+wAAAdFb3rCyeJxjYGRgYOBikGPQYWB0cfMJYeBgYGGAAJAMY05meiJQDMoDyrGAaQ4gZoOIAgCKIwNPAHicY2Bk+8g4gYGVgYNVmD2FgYGxCkKzCjK0MO1kYGBiYGVmwAoC0lxTGBwYKn4c4Cj/+4LhM0c5kwRQmBEkBwDIaQw3eJzN1DtP22AYxfF/Ejf0Qtu0TWmb3unFvYW5YurCwBdATA1i4AvAwMDEwILYmLIhkNjZEAsSTEhsiIUFOzXGwsFIdoCNHvOwd4pUR7/ItuQ31nvOE+AWUJIf4ui0j4LOKFZ0t3B9v8Td6/tO4Y+uf/NLz7xh+nDeK3mut+EX/YY/5y/4zdZSay8YCoaD2aNmWA0Hw9Xj0ciJ1qKDk614PF6Jt9u1tns6llSSRrKcrJ/NpPV0JJ3KJrPdbL8z0dk5X7woX25eXel3ur1+946C9qh7n3z9ojJxlEKZHm5zR/nco5f7POAhFR7xmCdUeUofz3jOC2q85BWvldpb3vGefj7wkU98xuULX/nGd+VcZ0CLl7u6N//YuP/k6M2/ij9vrrQrTN/QKx7OG6WAVzL5BHmuyafI2zD5dPlFo7TwG0a54c8ZJYi/YJQlftPkU9daMsqX1p7J3y4YMsqcYNgofYJZox5w1DRqBGHVqBuEg0YtIVw16gvHo0bNIXKMOkS0ZtQmogOjXnGyZdQw4nGjrhGvGLWOeNuof7RrRk2k7Rp1ktMxo3aSVIx6StIwaizJslF3SdaNWszZjFGfSetGzSYdMeo46ZRR28kmjXpPtms0AWT7RrNAZ8JoKujsGM0H54sm/6e8KBvNDJebhoG/YToZWwB4nFVYD1hT57k/73dOzkFEmoQQ0HEZ4b+IjJGQIDfjQaZIGaM8ljIuZVzqGKOMUkspZZRS6liapogxjTRS6ihFR6mj1jnnlDq0PI4yb6vUS6ml1iqlmeUyRWcRznm530lAW8I5J+eQ8H3v977v78/HAMMsTjNJjIYhDGPSB2pCNbEM/QH5xG3hVzG+9IYwbISaCdAl67gtt/CfurNRoPlKYthxhRMLpHX4NajIALz8x6XvEZH/gfw9ncofhGRjpEmvIqkJn/78GQj+SbZifUJN0GD4now755fHEXzoON+TP28wRfACREB0TIQ2UBWh0oE2SG80gU7Fb7xPsUaD8DgSdQjv+ze4D943qARDIJwHwpHnDm+PX3iUa4t9tuoDUeBXLVxs2LRLz4XfuckwPI1RIYzzpxiBCWZCmVgmnkmkQ+tUEcm6wAiWDqPSRITHRMdo9UnJKp1Cp6KPQRcdY9IG6QJ1QA+WfhKaFGqXGOrKcvEX3Du6/TTHtjXMF4M/a5V87NIk64yPbd9gZH89l6c4J4ayVwYkF/cVBqeniRzbJxXe5jYV+TcQZQuWFPDmhzaaf/F4yyJzSBzp6/OsA94ULvJ/ZL5Pb3iBAToHnbwCyToVoetBp0vf6eWnjHDRkI8heBlG0NiJ0XBxUbqRayQbYI34CVveyZaLH0EagKEQniJbRHcrlkNHKxuMHMZmJ8BHZIUTKtDllLzjLj4uTHjHNek8w+l4gY4XEMQLSwMuH7Fsl2QmQ9L13/0xLgPW9PQkp8Opg0SUOPrQzFbM5SgAO+CD66czssEMw/EOC/RiYQcmdSBpZzg61kPCFP82o2RCGD2TSoeny8oLXJAQGcUromMiV4BnCt7hwGjiBV4RI19i1AFBhDUZTUEM0M8Gcgo2kR3acQjWf1O+yOD5GdwVm0IyoUysJamYy85hIUmcn8OqoWt+/G3sjnz19dOV0RePu46fvJn7gBMRY6ELQnm8jhbFX+yOE12vtlsP9b63OyvjJIzMJ4DbbsdgO+ldE52fHm52dt30W2GFcOg1YwdO8s+9nI2lkn9+1taMlDJPydP83RCc/ItMFJPGeJIVCDqWzj/GU1hBWpMxIMKTyOWLLhnUAXeTqqK1RpedZpwI0XyYxHFacYS1R/tmZx7L7/LXNjv61GqNu1RypySCmHulEvPjDdC0DWel6LECnAKDHUJwssBSX1dZa69yhShetjtQKfm68wsJX5Cv5vjj12BQqsLaXCNUkUSMx6GMNAiGehf6QBY0W8GK9Vbsz3JYy1utC7NcPtrHC2QYoLHdERr4B5nVtEp+QDPHgFKQi8RoMq6mGaM3d5sHPM3D0rjoSx+o875oNaugPj7RlZrSFBvGd8+19fsEn65om+8Aji2U0l09hGARHOiEA1hEuIUStkwaZ59A7qR7LNs8eLoXulmfO0OIHOHN5X4WhUPslCab2ZER66FD1hGrdAb88Bad6wpPH13m32CCmAgmhTEz6cwmJovJZfK91eZpedV3pqcCPc2Bnj6mL1h+fBcRfgQ6OZ0KekTpAteSZB3ryRV48IE/gDY7ttkJkTpJmZ00S82En3OPOAcHnSNwjSNOyMCT12t6fZTdTdULyMZCHdokhBpsY+vRBnWiVX6fWmRvLq1jU+pb0hyV8GF1c3M7q2xpdrubW6Rg0kUM0ln7goablmpra5unrnDp+f5Vo3DFarWixSLGlZWUV5YpBjPM5WlGxpuzxRWCm3+LrsJ/MhuZLXJN0u6hPR2ou9fY34a9ZKMpglV7U2ky0jOtThmAAomgVZjUQQKJol+PMZI5WPfDBFf8OiKJHz5cCDkumEX/aUuDn7q1ogn5Xz08l5B6O7dRGbKtwJYY4irKRrGdpFsje9jmpoG6HQeltB29LssBxc5WR9yzT7fd+QIKsdcuNVwjW/OVTaTIceW2OIldCf5+WwuCffxmu89ALITeqRHWtGJ61fjtkkXmTCGET+fNDRYdo7GyNOf/FK7z+xkVrc8oGqlepWTVcjsRGVQC1CylEUaQJx9DAzeCNkAgMTzf0zY3Yfufs19hYkIazPUf5yQn74thdRnmmhLSMwE+lp7Ozmb+aXRJH+OJRWauCb/E18+k5bghCeJJkaTcYcbR3ATjvvw6RfV8ZYui+AKOF4LhggcPvqR1qKDMGsPQZjcGeHCNyOu/1P8KvUqj1yVRUKNlJPBrIUyVzirjfKQCvlCc949mR0U/l5Qfn07yj0gajul2gNqqVvrkFGuUayiCHcB5du85YDo7F5lznVIxtm7KhjhSapdm99XVHA0JPVM2DBovt9wRpvlXGS1D20KeiFqlV7J0JmoFpRqWzieE3bBR7GN/ruhXsE+LljZWW54kPTXcKeljH4PHyeedsApUeBP/1Sl+sbgtHXjye+l1dBjvaYXNfAzlVgYM0RHhvJCcBvokLlDDC/5EbqdkQxqY0oB9aJ+1dOihnFM7RoF57eTp3xpYIibd33v46O+4p5/dte3hkw/kfzH41vxvLbWVOf0/tZx4p7H5lPzvFTSGq8Ik5algJoHZQLs6k67qMn7S3g38Nn6COshI+YLWLS9ExniYxRS9conR5Qwo6B9pgUd5vhQyWoAzEOxwuzPbjFVppY4Kyxp2umqfs7SjpeMKFCUa0XVxCi2xKVBzqa/2AAmJy7LkGneQHQs5EG07NGjOOEfCqi4ONfTDO1AOpTbYh9tsx41H8vNKbAsVXDz2DxVAP04ePQoJKXhgcKA0tbhpcMKRnrfj7CBkkgM1zlRbY2pr/CY8h3Fx4HOkyH2rYta7tosgnOWB8ZerSOYJRiFEgtyYBsElGophBIx1OIJ5R8VrPPRgTjPOjnfPgM9CJV9MFQ+DC0IW/2NmJV25ECaMifToH8aLc14F5FVCKjUtS7UKPIpHdfeQBQFRkkwn/RV9nOjm85zzExzOG9MuKQbmJxSRaITDmOs9RJ/l96xpcnJhqLZWyJIc1dhNiac/Ix1iSQiZdS/EUt7pQjeWQrAVgmmcPnSenwnnPDokillL9ZlhCb09XJp8F7Dvccry7BUmTl4R+nc2iJNT7Y1ARutkz/whjDjFFhKKYXDZRWJdcBnDSLjYSNrbFyrb2bZU6IXwdLSJsyRWGucLsQf7Q+KggnMh7WPvIVUCIpEP9sl+66B1gP7QS784ZDZvq99eZm1SpA7OTza1F5tzCtmkARwaaB5An4ElbbA4xf0X7Q9fRk2zqGR0YSolExFO38rvdGEPgxIITOPX89MoDcMGMOAoniJu6ID94hTW4yNgg+elV8iT5EVvTbxE1+oN5r67mu2uThsg10QrW3+ErRNt5Nqd+nVsyQFSK7UeELu7lrBSon30Kq0FE/MjD1Z6vutFggjVEhhRqExWLRUGS1GLLBMFlTG6ALk0IiGIUZBzMx3sdun8q3Ao14Apu9+pHPBXW05nx1VlzUgW0uzEc2EwFuwfLG496qftL21Ra/0wOhWOoYYzQgHE1eFZ7GQfYHPEI3YMWsxJhweJTtpqqCrO2FRriLNllRAH2yiVplG0qzmOU3xOibKlE9aQStiKthEI2Y5TE964Fr/iHqBrHEwZj9Z3gMFoSgAZdpJCQcahUFD6Q1gCmDQ0CmOyITqMD9Bok4yG6HB+W1fTL+ueeP/myPYny5v2Nbnx86nmwb6dtrffwRuHUpwX9r782W44ZLmSuOFwRfXRil8dfbz8T6k/vILfnK+tHW21HXjzhea33yK5FXvazzl2efLzmHBScYMJuKepk7+lozOouikgfZIv3yXx5LiUSaVzyypS0UXMXV3SUJfk6lrC1cUvuVDqjShuUyCnKUjWhhmVFGAFGQpYUxLHheJHePHXr8Hmv3/4ruOpDeSCdD5s521YDZeu4rWNw+V/gtj9q1j1Qbyf//fSOoHQyP+B9pnXBZFvMyWV2OogD6ouQ6XMpUvyTptMbyI4TfbopMN2oHscR2OzIW1sfLRxvN9WIh4hsZk5trKUahJN0vbNVI75qbtrOjDB5eLeRwc24sho5ewUHppOyZ2hqU8AbRFOXgMGyh22xsyu2hQHHL3TgSIh/NZSDXEpqhaUSzw6xe9h1slYQOem5wVt0PKaftefqLRBXBS1E1GRrEwCJnWAxzWoKduzhJUFDQnp9HNy6oIeKnmH0A7bXbL2gD60yNc6JyDxj9Qgg76o6U+pjmVH648f7qxpbzt67JC1q/PIeFra7PGzT1H6Cz7oHKlguVZIaQVfvN2Kw614spWSBOH9i7IIp4E8xP4Svikfx/ASxEOOAWvxIMX3sTLQAo8fLDIZsRAGm6BoSWOfp3GupwgRziRThltiN69akzUrFdygM3keCR5hRvtTTo5Jtk/e/JmMqqgIlZ6f2obz5AyOGrOhES1WQ6qBrYQMI8ZyFulWGkw7pGIHuBxULpjHK3D6ugUrExPAUp0prZmdJTqwwJmWFvdZcVMzEStKzOTYfGvr/MIMaxEbWA4/wMu9Oee6bZcP4u2u7DTnRCtoR6QcubZoIB20Xu+jMoP6SZqcJK3ce4FyC3IRoPJ0no71XJW6Yfj72Vu7n9v3Ln5xGf99dPd+nBi+/tpb+Aq/6r3Xm4fWcup/dA5/oyjB7+189lPpMWly9/Pgu4ynmbTXZY3PmGg/q1V8DE8BNdnA6JMYCq668JiA5UaneuSvzc5zXxJSfuO9RQaCP/8KODyEH7/xxBNdOxsO7H/h2Z7RbGqBEgg5DX5jkxCFe3A/PohJyVxI51/+8PQfPj25hJ1XaY5ep7GlM5s9fuI7RUgUXsHBeQUHqzCaVHcFCkVWTZCg0tzzSrwAOipUCFLvcJv4dpEw6TL07UTxC8ih1XLiCt7Brrh0+KV06XFxzys78Tb4dly79uRj3ORw3nY//zpzwQsv8tul54tGp9mgFkhyyFbDgR/U4/a5d35emNHy7pmX0nNrj82C1bkuDt62QQs22vD5qMhS8/3SMxcIIfkFfkUkcf0PIBWHLl72rC0VWy/SHAoyu+iok2NpmQXQ7ongBVbx4mf7pGf2fEZyx/ZcW7lKsdLfLTt8fpWYTVq+/9PMaKnRW8s3hAnKMWEUY5Iojy8rNdkzRsouQl6w7yi29bQ2VFFBCnqnCPDaK885eLIWhyCrw+q/BlqgyXCkG9LwdKG9YXtzTXtddzjpZZUdYPbDYx0Sc6n4kq2iDQdKJ2srSiCIivT6NohW+mVnh5idwWocbruS11hXY68U41kLnh3bejqTu7CQGmoPlQ6SzEyupqyvuc6BI+WHKxu2efF3iltN60xHI9B6azYiWR+mMujChWSjnha3UuGpbRmbd/1+uOsEPvz8M/AUXn3D7vrHmes40vsefjQ/8QKwz7zWAtHdoFms/mvhh/vx3M849fvt5xeZrct1Nc5vpmsezkTf25kCWkzgBWa6ekbTMhwE6hgPBUcrjrgWGl384dRwqR6nj0gF2gyyb584weZrecouFon3UbJtoh3ihxcauRZ+s1STn78wlpddCE50tJmLGsDQWm5pbbWWtaKN98OxJb1Ck2ijNeBHHRUDS9aYGkTGsxNH2G63+6S0/hRYnkMtfFMxQ/MP3eiEqr2fEOMdEciVE/i6vO+G/yfU8ltoXBHUBa3z7h0ELEUn0IgomMviQucRF2HUCemIQo522XCD13BP8QbXvOhqIqMrV3Sv9GX3atTRODo44qOdgEqt0k+cv19aW0GcD0qbQUuM0gj5wHP2HPOifOW3iJn5+Z25pb/4CaITB3w2VQUfrrHh5nfte+EBwrndbqiemlryzvgvqrn/SqP/Hs099W+w5BtUSlkjr6ZOgrauzC30WYBJJhjwnNmjjoLcR9h1d67hROKm62zuRmkX+1rn2/0ndsPMneEqV2NtXzGUdlTkHUrlf51b3ZziQq1kxu6MLPAjVmKppqu3i/w5kcrlZhdXbaBTNRuglfjEowszEqB1CYe+Fkqpt7+PKowgz4rqVV4NH+HdulStJSpdL0sOsr49UsdBqbuH10gdpHzeTkqkbu4bOII54vYqKZi4q4iIHIhLe1j/Es7wb9KowxnZZkR5kCwqMkrtLUDv9gEBTpaEHLXUxdX4Z3wJP5aei0wlW+A/qKQftVZSQNMXbTyc9xPuTfzvn+HnULpLerT6l0DmIeKx9lPvXn0zs+j5d196kdr6NU68FTl/wSndwE/62Ms4Pl77NAQysm9ZXC3c4vdSPRfucQOpFHPlXQxWL8+F1VNK131bk95LCAh3bS212bIbCPJuX3jOCmMUT+MAQ8KIAVNJSVqTvx+PWOXwVdq3t/r4+WBYOskgo/btrroWKF1IJGPRs1CeHoddl86iIzId2i5gL5siDs+25RsdqVjcui3DmSGWumnpcZOoiJIukm6rOIZFeB3P8dn56r4J6vH6549DGbQkYgf224RN6bh1KM8MHFRjO142ZIMGhqQwW100XrgcB5rueJy8lASMJiEjLy0xc4nzHqZYpJVzA5TUCKunEKT2gI+H8pKC4FuUx87/puX9W0RRfeP96/j1x9N4Ex6BsP0lUt4bLzR3vfJSS48iMw278fz/4vwnV3ECnoAHqd+4ul6EvRcHnF2Hj9zz9isoFqxkmLVwT21xK8S/saFSH4mTxshv+FWHUfmO9I1nnuDhyNXMD+XKTJZdWKAi8Du7TT8C6iG8To6RGVO2s4zXuqWzndAgZnI9aJBNwUzdAK8+3FArlm1lo+1stGSmZs1piJUQB+3olsaDM4kPhEu58GTBoLVrck0rile4TeXqiivc2ZkZKsuKtmYchBSspYg3ccm8td8TkWdP5CrlqP2UoxjgFBRwZHiVSytALxcR65FZgUD7noki/rAC9DC00PUIRpDVVdK/yZZHjz7K/klUVXGfzv/zEa5Nmra0baOyMQx+WrcbXnDOuUDtkpWhC2dctztxQ/pmF/jIVuX/AcSzTkYAeJxjYGRgYADimhbvinh+m68M3BwMIHDjUmMFgv53kYOB7SCQy8HABBIFADqiC2YAeJxjYGRg4Cj/+4LhMwcDCABJRgZUoA8AYu8DmXic42AAghQGBpaNEMx+kYGBg4F4DNKDTwzGRlfHyooQY12IXy2yWSxpCD4A7W4KaQAAAAAADAAoAEAAcgDEAQABNgGkAhICaALsA2IDrAPyBCIEVATQBPAFRAWyBdoF+AZkBqoGzgb4B1AHxAgmCFoIlgkICSoJjgnCCgoKLgqKCtoLBgtMC9QMEAwoDHwMunicY2BkYGDQZwhl4GQAASYg5gJCBob/YD4DABZbAaQAeJx9ks1Kw0AUhU9sVWxFQcGVyqxEUFN/du5E0W6K0EWh3aXpTI2kmTAZCz6H7+DT+Azik4gn6VWpQjPk8t1zz525AwNgC+8IMPv2+M84wCazGS9hFcfCNWzgQrhOvhJeRhP3wivUB8INHOFBuIltvHCHoL7G7BKvwgH28SG8xN5P4Rp2g3XhOvlQeBk7wY3wCvWBcAO9YCrcxEHw1lDq2unI65EaPitjM38SR84l2rHSSWJnC2u86kdtnXT1+CmN3I9aifNZT7sisZk6C0/nC3c60+77mGI6PvfeKOPsRN3yTJ2mVuXOPurYhw/e55etlhE9jO2EcyuuazhoRPCMI+ZDPDMaWGTUThCz5rgS1p30dJjFzCwK/oY+hT59bXoSdBnHeEJadf73/joX1XrVeQWpnEThDCFOF3bcMWZV19/bFJhyonOqnj3l7codJqRbuafmtClZIa9qj1Ri6iFfUdmV8920uMwff0gXd/oCX7iEuAAAeJxtkEdXxDAMhP0tLEvvfem9b+ISO8fdxPklXLhw4z1+PkTiiA/S02hG0tgMjL6x+f9NGDDHPEMWGLHIEsussMoa62ywyRbb7LDLHvsccMgRx4w54ZQzzrngkiuuueGWO+554JEnnnnhlTcmFIbv4dfnh4sSyz7699FvrKdt6nMVbdPnGMpOcm46xSvpB/+XXZiKrvJS+5yD8EIupF9b3WEFTbZUVjGTbuNVnRsvLNWkrN3OFoLK5OjSTCqZH2wpaGqj1DGFIC6scGrZZpPoveyMdSs+ndP7nW706tJFQXPt9T7b6vXR6a+kRtiVzFOH0Wflls6YH1WNYlgA"
    b=b"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"
    font_data_decode = base64.b64decode(a)

    with open(path, 'wb') as f:
        f.write(font_data_decode)

    font_data_decode2 = base64.b64decode(b)

    with open("2set"+path, 'wb') as f:
        f.write(font_data_decode2)

def save_font_file(url):
    conn_text=rq.get(url,headers=headers).content
    conn_text.decode("utf8")

    match_font=re.search(rb"base64,(.*?)\)",conn_text,re.S)
    if not match_font:
        raise Exception("not find base64 code")

    font_data_old=match_font.group(1)

    font_data_decode=base64.b64decode(font_data_old)

    font_file_name="font_new.ttf"

    with open(font_file_name,'wb') as f:
        f.write(font_data_decode)

    return conn_text

def generate_font_xml(path):
    font=TTFont(path)
    font.saveXML("font_old.xml")

def parse_font_xml(path):
    font=TTFont(path)

    font_dict=['2','士','E',"B","届","技","中","应","0","张","6","大","A","M",
               "女","1","下","验","陈","专","科","刘","黄","周","以","高","李",
               "生","3","无","王","博","本","4","吴","杨","5","8","硕","9","男",
               "校","7","经","赵"]
    font_name=font.getGlyphOrder()[2:]
    font_code_to_value_dict={}
    for i in range(len(font_dict)):
        current_font_name=font_name[i]
        font_code_to_value_dict[current_font_name]=font_dict[i]

    return font_code_to_value_dict


def generate_new_font_map(font_new_path,font_old_path,font_dict):
    font_new=TTFont(font_new_path)
    font_new_orders=font_new.getGlyphOrder()[2:]

    font_old = TTFont(font_old_path)
    font_old_orders = font_new.getGlyphOrder()[2:]

    font_dict_for_new={}
    for new_order in font_new_orders:
        ojb=font_new['glyf'][new_order]
        for old_order in font_old_orders:
            ojb_old=font_old['glyf'][old_order]

            if ojb==ojb_old and len(new_order)==7:
                font_name=new_order.replace("uni",r"\u").encode("utf8").decode("unicode_escape")
                font_dict_for_new[font_name]=font_dict[old_order]

    return font_dict_for_new

def run(url):

    conn_text=save_font_file(url)
    # generate_font_xml("font_old.ttf")
    font_old_path="font_old.ttf"
    font_new_path = "font_new.ttf"
    font_dict=parse_font_xml(font_old_path)
    font_new_dict=generate_new_font_map(font_new_path,font_old_path,font_dict)

    sel=etree.HTML(conn_text)
    names=sel.xpath('//span[@class="infocardName fl stonefont resumeName"]/text()')

    if names:
        for name in names:
            for i in font_new_dict.keys():
                print("name old:",name)
                name.replace(i,font_new_dict[i])
                print("name new: ",name)

    # generate_font_file()

if __name__ == '__main__':
    url="https://su.58.com/qztech/"
    run(url)