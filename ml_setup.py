from model_train import *
import sys
def ml_setup(city):
    name=city.lower()
    data = prepare_data(name)
    mae, r2, predictions = train_model(data,name)
    print(mae,r2,predictions)
    

if __name__ == "__main__":
    if len(sys.argv) > 1:
        city = sys.argv[1]
        ml_setup(city)
    else:
        print("Please provide a city name as an argument.")
