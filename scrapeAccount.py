import got3 as got
import sqlite3

def scrapeAccount(account):
    tweetCriteria = got.manager.TweetCriteria().setUsername(account)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    
    conn = sqlite3.connect("tweeter.db")
    curs = conn.cursor()

    curs.execute(f'''
    CREATE TABLE IF NOT EXISTS {account} (
    id INTEGER PRIMARY KEY
    ,link TEXT NOT NULL
    ,content TEXT NOT NULL
    ,date TEXT NOT NULL
    ,retweets INTEGER NOT NULL
    ,favorites INTEGER NOT NULL
    ,mentions TEXT
    ,hashtags TEXT
    ,geo TEXT
    )
    ''')
    
    for t in tweets:
        curs.execute(f"SELECT {account}.id FROM {account} WHERE {account}.id = {t.id} LIMIT 1")
        
        if len(curs.fetchall()) != 0:
            continue
        
        insertQuery = f'''INSERT INTO {account}
                          (id, link, content, date, retweets, favorites, mentions, hashtags, geo) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);'''
        
        
        data = (t.id, t.permalink, t.text, t.date, t.retweets, t.favorites, t.mentions, t.hashtags, t.geo)
        
        curs.execute(insertQuery, data)
    curs.execute(f"select count(*) from {account}")
    res = curs.fetchall()
    if len(res) != 0:
        print(f"{res[0][0]} tweets scraped, stored in table {account}")
    else:
        print("no tweets scraped")
    conn.commit()
    conn.close()

def main():
    print("Enter twitter account to scrape")
    account = input("@").lower()
    scrapeAccount(account)

if __name__ == "__main__":
    main()