import sklearn.metrics as metrics
import matplotlib.pyplot as plt
import numpy as np

# returns score values for f1, balanced accuracy, area under the curve and null accuracy
# also pritns roc curve for now it's here


def score(y_true, y_pred):
    f1 = metrics.f1_score(y_true, y_pred, labels=None, pos_label=1, average='binary', sample_weight=None)
    balanced_accuracy = metrics.balanced_accuracy_score(y_true, y_pred, sample_weight=None, adjusted=False)
    auc = metrics.roc_auc_score(y_true, y_pred, average='macro', sample_weight=None, max_fpr=None)
    null = max(y_true.mean(), 1 - y_true.mean())

    fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred, pos_label=None, sample_weight=None, drop_intermediate=True)
    plt.figure()
    lw = 2
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve (area = %0.2f)' % auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver operating characteristic example')
    plt.legend(loc="lower right")
    plt.show()

    cm = metrics.confusion_matrix(y_true, y_pred)
    plt.clf()
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Wistia)
    classNames = ['Negative', 'Positive']
    plt.title('Versicolor or Not Versicolor Confusion Matrix - Test Data')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    tick_marks = np.arange(len(classNames))
    plt.xticks(tick_marks, classNames, rotation=45)
    plt.yticks(tick_marks, classNames)
    s = [['TN', 'FP'], ['FN', 'TP']]
    for i in range(2):
        for j in range(2):
            plt.text(j, i, str(s[i][j])+" = "+str(cm[i][j]))
    plt.show()
    return f1, balanced_accuracy, auc, null

# function that will return score of the model with test sample, requires frame_size to be given so batch size can be given.
def score_model(model, y_test, x_test, frame_size):
    t = model.predict(x_test, batch_size=frame_size)
    return score(y_test, t)
