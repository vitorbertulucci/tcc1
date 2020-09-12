import rouge

class RougeMetric:
    """
    Rouge Metric class to compute both Rouge-N and Rouge-L summarization metrics;

    Parameters
    ----------
    - max_n: int, optional, default to 4
        Defines maximum N value to Rouge-N metric
    - alpha: float, optional, default to 0.5
        # TODO: describe alpha argument
    - weight_factor: float, optional, default to 1.2
        # TODO: describe weight_factor argument
    - batch_size: int, optional, default to 1000
        Defines the size of the batches that the data will be divided by.

    Attributes
    ----------
    - data: array
        Stores the loaded data value containing file reference, original text reference, simple image processing reference, GAN processing reference and Decrappification reference
    - computed_data_size: int
        Stores the count of processed data
    - rouge_instance: Rouge
        Instance of Rouge metric
    - BATCH_SIZE: int, imutable
        Stores the batch size
    """
    data = []
    computed_data_size = 0
    rouge_instance = {}
    BATCH_SIZE = 1000

    def __init__(self, max_n=4, alpha=0.5, weight_factor=1.2, batch_size=1000):
        self.rouge_instance = rouge.Rouge(
                metrics=['rouge-n', 'rouge-l'],
                max_n=max_n,
                limit_length=True,
                length_limit=100,
                length_limit_type='words',
                apply_avg=True,
                alpha=alpha,
                weight_factor=weight_factor,
                stemming=True
            )

        self.BATCH_SIZE = batch_size


    def compute_metric_value(self):
        """
        Get stored data and apply both Rouge-N and Rouge-L metrics to it.
        It consider both computed_data_size and data class arguments to compute only remaining data.

        It changes the class data attribute to an array object keys to contain:
        - text: current data reference text or original text
        - rouge_metric: contains the result of Rouge metrics
        """
 
        start = 0
        end = len(self.data)
        if self.computed_data_size % self.BATCH_SIZE == 0:
            start = self.computed_data_size
        slice_obj = slice(start, end)
        print(slice_obj)
        for data in self.data[slice_obj]:
            # print('Evaluating data for "{}" file'.format(data['file_reference']))
            data_reference = data['reference']
            for key in ['simple_processor', 'gan_processor', 'decrappification_processor']:
                data[key] = {
                        'text': data[key],
                        'rouge_metric': self.rouge_instance.get_scores(data[key], data_reference)
                    }
            self.computed_data_size += 1
            print(self.computed_data_size)


    def store_data(self, file_reference, reference, simple_processor, gan_processor, decrappification_processor):
        """
        Store loaded data as an object containing.

        Parameters
        ----------
        - file_reference: str
            Path to original file
        - reference: str
            Original text of the file_reference
        - simple_processor: str
            Text containing the OCR result of images generated by simple image processor
        - gan_processor: str
            Text containing the OCR result of images generated by GAN model image processor
        - decrappification_processor: str
            Text containing the OCR result of images generated by Decrappification image processor
        """

        data_length = len(self.data)
        print(data_length ,data_length % self.BATCH_SIZE, data_length > 0)
        if data_length % self.BATCH_SIZE == 0 and data_length > 0:
            print('echa')
            self.compute_metric_value()

        ref_dict = {
                'file_reference': file_reference,
                'reference': reference,
                'simple_processor': simple_processor,
                'gan_processor': gan_processor,
                'decrappification_processor': decrappification_processor
            }
        self.data.append(ref_dict)
