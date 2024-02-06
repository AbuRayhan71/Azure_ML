from azureml.core import Workspace, Dataset, Experiment
from azureml.train.recommendation import Recommendation
from azureml.core.model import Model
from azureml.core.webservice import AciWebservice, Webservice

def main():
    # Connecting to  Azure ML workspace
    workspace = Workspace.from_config()

    # Loading the data
    datastore = workspace.get_default_datastore()
    dataset = Dataset.Tabular.from_delimited_files(path=(datastore, 'path_to_your_dataset.csv'))

    # Spliting the  data into training and test sets
    train_data, test_data = dataset.random_split(percentage=0.8, seed=123)

    # example
    experiment = Experiment(workspace=workspace, name='event_recommendation_experiment')

    # recommendation model
    recommendation = Recommendation(source_directory='.', 
                                    compute_target='your_compute_target',
                                    rating_column_name='rating',
                                    user_column_name='user_id', 
                                    item_column_name='event_id')
    run = experiment.submit(recommendation)

    # Monitor your run
    run.wait_for_completion(show_output=True)

    # Register the model
    model = run.register_model(model_name='event_recommendation_model', model_path='outputs/model/')

    # Define the deployment configuration
    deployment_config = AciWebservice.deploy_configuration(cpu_cores=1, memory_gb=1)

    # Deploy the model as a web service
    service = Model.deploy(workspace, "eventrecommendationservice", [model], deployment_config=deployment_config)
    service.wait_for_deployment(show_output=True)

if __name__ == "__main__":
    main()
