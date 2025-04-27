def logs():
    main = 0
    get = 0
    post = 0

    with open('logs.log', encoding='utf-8') as file:
        for line in file:
            if "GET / HTTP/1.1" in line:
                main += 1
            if "GET" in line:
                get += 1
            if "POST" in line:
                post += 1
    return {
        'main_page': main,
        'get': get,
        'post': post
    }


print(logs())