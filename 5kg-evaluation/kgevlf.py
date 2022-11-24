import ampligraph
import numpy as np
import tensorflow as tf
from ampligraph.latent_features import ComplEx
from ampligraph.latent_features import TransE
from ampligraph.latent_features import DistMult
from ampligraph.latent_features import HolE
from ampligraph.datasets import load_from_csv
from ampligraph.evaluation import train_test_split_no_unseen
from ampligraph.evaluation import evaluate_performance, mr_score, mrr_score, hits_at_n_score
from ampligraph.utils import create_tensorboard_visualizations

X = load_from_csv('.', 'kgmat.csv', sep=',')

print(X[:5,])

entities = np.unique(np.concatenate([X[:, 0], X[:, 2]]))
relations = np.unique(X[:, 1])

X_train, X_test = train_test_split_no_unseen(X, test_size=40495)

print('Train set size: ', X_train.shape)
print('Test set size: ', X_test.shape)

nepochs = 10

model_ComplEx = ComplEx(batches_count=100,seed=0,epochs=nepochs,k=150,eta=5,optimizer='adam',optimizer_params={'lr':1e-3},loss='multiclass_nll', regularizer='LP', regularizer_params={'p':3, 'lambda':1e-5}, verbose=True)
model_HolE = HolE(batches_count=100, seed=555, epochs=nepochs, k=150, eta=5,optimizer='adam',optimizer_params={'lr':1e-3},loss='multiclass_nll', regularizer='LP', regularizer_params={'p':3, 'lambda':1e-5}, verbose=True)
model_DistMult = DistMult(batches_count=100, seed=766, epochs=nepochs, k=150,optimizer='adam',optimizer_params={'lr':1e-3}, loss='multiclass_nll',regularizer_params={'p':3, 'lambda':1e-5}, verbose=True)
model_TransE = TransE(batches_count=100, seed=899, epochs=nepochs, k=150,optimizer='adam',optimizer_params={'lr':1e-3}, loss='multiclass_nll',regularizer_params={'p':3, 'lambda':1e-5}, verbose=True)

positives_filter = X

tf.logging.set_verbosity(tf.logging.ERROR)
model_list = ['ComplEx', 'DistMult', 'HolE', 'TransE']

file_writer = open('results.csv', 'a+')
file_writer.write('Model,MRR,MR,Hits@10,Hits@3,Hits@1\n')

for modelz in model_list:
    if modelz == 'ComplEx':
        model = model_ComplEx
    elif modelz == 'DistMult':
        model = model_DistMult
    elif modelz == 'HolE':
        model = model_HolE
    elif modelz == 'TransE':
        model = model_TransE
    
    print('Training model: ==== >', modelz)
    model.fit(X_train, early_stopping = False)
    
    # model.fit(X_train, verbose=True)
    print('Model trained === >', modelz)
    print('Evaluating performance...')
    ranks = evaluate_performance(X_test,model, positives_filter,use_default_protocol=True, verbose=True)
    print('Evaluation done')
    print('Computing metrics...')
    mr = mr_score(ranks)
    print('MR: ', mr)
    mrr = mrr_score(ranks)
    print('MRR: ', mrr)
    hits10 = hits_at_n_score(ranks, n=10)
    print('Hits@10: ', hits10)
    hits3 = hits_at_n_score(ranks, n=3)
    print('Hits@3: ', hits3)
    hits1 = hits_at_n_score(ranks, n=1)
    print('Hits@1: ', hits1)
    print('Metrics done')
    file_writer.write(modelz + ',' + str(mrr) + ',' + str(mr) + ',' + str(hits10) + ',' + str(hits3) + ',' + str(hits1) + '\n')
    print('Model: data write completed === >', modelz)
    # create_tensorboard_visualizations(model, X_test, ranks, positives_filter, 'logs/' + modelz)
    try:
        create_tensorboard_visualizations(model, 'logs/'+modelz)
        print('Model: tensorboard visualizations created ===>', modelz)
    except:
        continue

    # create_tensorboard_visualizations(model, 'vis_folder_name')
    
file_writer.close()
