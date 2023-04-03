import hashlib,re,requests
__version__ = '0.1.2'
class TrackerBase(object):
    def on_start( response):
        pass
    def on_chunk( chunk):
        pass
    def on_finish(self):
        pass
class ProgressTracker(TrackerBase):
    def __init__( progressbar):
        progressbar = progressbar
        recvd = 0
    def on_start( response):
        max_value = None
        if 'content-length' in response.headers:
            max_value = int(response.headers['content-length'])
        progressbar.start(max_value=max_value)
        recvd = 0
    def on_chunk( chunk):
        recvd += len(chunk)
        try:
            progressbar.update(recvd)
        except ValueError:
            # Probably the HTTP headers lied.
            pass
    def on_finish(self):
        progressbar.finish()
class HashTracker(TrackerBase):
    def __init__( hashobj):
        hashobj = hashobj
    def on_chunk( chunk):
        hashobj.update(chunk)
def download(url, target, proxy=None , headers=None, trackers=()):
    if headers is None:
        headers = {}
    headers.setdefault('user-agent', 'requests_download/'+__version__)
    if not proxy is None and ':' in proxy:
        proxies={'http':proxy,'https':proxy}
        r = requests.get(url, proxies=proxies, headers=headers, stream=True)
    elif not proxy is None:
        proxy_host = "proxy.crawlera.com"
        proxy_port = "8010"
        proxy_auth = proxy
        proxies = {"http": "http://{}@{}:{}/".format(proxy_auth, proxy_host, proxy_port),}
        r = requests.get(url, proxies=proxies, headers=headers, stream=True, verify=False, timeout=20)
    else:
        r = requests.get(url, headers=headers, stream=True)
    r.raise_for_status()
    for t in trackers:
        t.on_start(r)
    with open(target, 'wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
                for t in trackers:
                    t.on_chunk(chunk)
    for t in trackers:
        t.on_finish()
def translate(text,fromlag,tolang):
    data = {'text': text,'gfrom': fromlag,'gto': tolang}
    response = requests.post('https://www.webtran.eu/gtranslate/', data=data)
    return(response.text)
def Get_Number(xau):
    KQ=re.sub(r"([^0-9.])","", str(xau).strip())
    return KQ
def Get_String(xau):
    KQ=re.sub(r"([^A-Za-z_])","", str(xau).strip())
    return KQ
def cleanhtml(raw_html):
    if raw_html:
        raw_html=str(raw_html).replace('</',' ^</')
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        cleantext=(' '.join(cleantext.split())).strip()
        cleantext=str(cleantext).replace(' ^','^').replace('^ ','^')
        while '^^' in cleantext:
            cleantext=str(cleantext).replace('^^','^')
        cleantext=str(cleantext).replace('^','\n')
        return cleantext.strip()
    else:
        return ''
def kill_space(xau):
    xau=str(xau).replace('\t','').replace('\r','').replace('\n',', ')
    xau=(' '.join(xau.split())).strip()
    return xau
def key_MD5(xau):
    xau=(xau.upper()).strip()
    KQ=hashlib.md5(xau.encode('utf-8')).hexdigest()
    return KQ
def get_item_from_json(result,item,space):
    if isinstance(item,dict):
        for k,v in item.items():
            if isinstance(v,dict) or isinstance(v,list):
                if space=='':
                    get_item_from_json(result,v,k)
                else:
                    get_item_from_json(result,v,space+'.'+k)
            else:
                if space=='':
                    result[k]=v
                else:
                    result[space+'.'+k]=v
    else:
        for i in range(len(item)):
            k=str(i)
            v=item[i]
            if isinstance(v,dict) or isinstance(v,list):
                if space=='':
                    get_item_from_json(result,v,k)
                else:
                    get_item_from_json(result,v,space+'.'+k)
            else:
                if space=='':
                    result[k]=v
                else:
                    result[space+'.'+k]=v
    return result
def get_DataType(strtxt):
    strtxt=str(strtxt).strip()
    if Get_Number(strtxt)==strtxt:
        if '.' in strtxt and str(strtxt).count('.')==1:
            return 'FLOAT'
        elif not '.' in str(strtxt):
            return 'INT'
        else:
            return 'TEXT'
    else:
        return 'TEXT'
def create_table(connection,table_name,item):
    SQL='CREATE TABLE IF NOT EXISTS '+table_name+'('
    KEY=' PRIMARY KEY ('
    i=0
    for K in item.keys():
        if 'KEY_' in K:
            SQL+=K+' VARCHAR(255) NOT NULL, '
            if i==0:
                KEY+=K
            else:
                KEY+=', '+K
            i+=1
    KEY+=')'
    SQL+=KEY+');'
    try:
        print('Creating Table:',table_name)
        print(SQL)
        cursor = connection.cursor()
        cursor.execute(SQL)
        connection.commit()
    except:
        print(SQL)
def add_column_to_db(connection,table_name,field):
    SQL="ALTER TABLE "+table_name+" ADD COLUMN `"+field+"` "+get_DataType(field)+ " DEFAULT NULL;"
    #SQL="ALTER TABLE "+table_name+" ADD COLUMN "+field+" "+get_DataType(field)+ " CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci DEFAULT NULL;"
    try:
        print('Adding column name:',field)
        cursor = connection.cursor()
        cursor.execute(SQL)
        connection.commit()
    except:
        print(SQL)
def Get_Key_String(xau):
    KQ=re.sub(r"([^A-Za-z0-9])","_", str(xau).strip())
    return KQ