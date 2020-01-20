import argparse
import os
import got3
import gpt_2_simple as gpt2

def fetch_user():
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help='Enter twitter username to scrape')
    parser.add_argument("num_fake_tweets", help='Enter number of tweets to save', type = int)
    
    args = vars(parser.parse_args())
    return (args["username"].replace("@", "").strip(), args["num_fake_tweets"])


def scrape_account(user):
    print(f"fetching tweets from {user}")
    tweetCriteria = got3.manager.TweetCriteria().setUsername(user)
    tweets = got3.manager.TweetManager.getTweets(tweetCriteria)
    
    with open(f"data/{user}.txt", "w") as f:
        for t in tweets:
            f.write(t.text + "\n")
    
    print(f"{len(tweets)} tweets scraped from @{user}")

def generate_tweets(user, num_fake_tweets):
    print("building gpt2 model")
    
    model_name = "124M"
    if not os.path.isdir(os.path.join("models", model_name)):
        print(f"Downloading {model_name} model...")
        gpt2.download_gpt2(model_name = model_name)   #    

    f = f"data/{user}.txt"
    s = gpt2.start_tf_sess()
    gpt2.finetune(s,
                  f,
                  model_name = "124M",
                  steps = 1000,
                  run_name = "run1",
                  print_every = 10,
                  sample_every = 200)
    
    count = 0
    with open(f"output/{user}", "w") as f:
        while count < num_fake_tweets:
            tweets = gpt2.generate(s, return_as_list = True)[:-1]
            for i in tweets:
                if count < num_fake_tweets:
                    f.write(i + "\n")
                count += 1
    
    print(f"{num_fake_tweets} tweets in the style of @{user} written to output/{user}.txt")        
                  
    
def main():
    user, num_fake_tweets = fetch_user()
    #scrape_account(user)
    generate_tweets(user, num_fake_tweets)
    
    
    
if __name__ == "__main__":
    main()