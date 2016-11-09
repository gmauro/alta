from alta.utils import a_logger, import_from

import os
import json

NO_BIKALIMS_CLIENT_MESSAGE = ('The bika client is required, please install it'
                              ' - https://github.com/ratzeni/bika.client')

COMPLEX_SAMPLE_TYPES = ['FLOWCELL', 'POOL']
ANALYSIS_NOT_SYNC = ['full-analysis']

class BikaLims(object):
    """

    """

    def __init__(self, url, user, password, loglevel='INFO'):
        self.log = a_logger(self.__class__.__name__, level=loglevel)
        BC = import_from("bikaclient", "BikaClient",
                         error_msg=NO_BIKALIMS_CLIENT_MESSAGE)
        if not url.startswith(('http://', 'https://')):
            self.log.warning('Must be provided a wellformed url to the Bika '
                             'server')
        self.client = BC(host=url, username=user, password=password)
        self.log.info("Connected to {} Bika server".format(url))

    def from_bikaid_2_samplelabel(self, bid):
        """
        Given a valid Bika id, returns a dictionary filled with batch id and
        sample label

        :type bid: str
        :param bid: Bika id
        :return: a dictionary with batch's id and sample's label as
        provided from the owner otherwise None.
        """
        result = self.client.query_analysis_request(params=dict(id=bid))
        if result:
            return {'batch_id': result[0]['title'],
                    'sample_label': result[0]['ClientSampleID']}
        else:
            return None

    def get_batch_info(self, batch_label):
        """
        Given a valid bika batch label, returns a dictionary filled with all
        the info of the samples owned by the batch

        :type batch_label: str
        :param batch_label:
        :return: a dictionary with as key the sample id and value a
        dictionary collecting the type, label and external label of the sample
        """
        result = self.client.query_analysis_request(params=dict(
            batch_id=batch_label)
        )

        if result:
            batch_info = dict()
            for r in result:
                sub_d = {'type': r['SampleTypeTitle'],
                         'sample_label': r['Title'],
                         'client_sample_id': r['ClientSampleID']
                         }
                batch_info[r['SampleID']] = sub_d
            return batch_info
        else:
            return None

    def get_analyses_ready_to_be_synchronized(self, samples=list(), action='submit'):
        """

        :param samples:
        :param action:
        :return:
        """
        def get_review_state(action):
            review_state = dict(
                receive='sample_due',
                submit='sample_received',
                verify='to_be_verified',
                publish='verified',
                republish='published'
            )
            return review_state.get(action)

        if len(samples) == 0:
            samples = self.client.query_analysis_request(params=dict(
                review_state='sample_received')
            )
        else:
            samples = self.client.query_analysis_request(params=dict(
                id=[s.get('id') for s in samples],
                review_state='sample_received')
            )

        analyses = list()

        for ar in samples:
            for a in ar['Analyses']:
                if str(a['id']) not in ANALYSIS_NOT_SYNC and str(a['review_state']) == get_review_state(action):
                    path = os.path.join(ar['path'], a['id'])
                    a.update(dict(path=path))
                    analyses.append(a)

        return analyses

    def get_analysis_requests_ready_to_be_published(self, samples=list()):
        """

        :param samples:
        :return:
        """
        if len(samples) == 0:
            result = self.client.query_analysis_request(params=dict(
                review_state='sample_received')
            )
        else:
            result = self.client.query_analysis_request(params=dict(
                id=[s.get('id') for s in samples],
                review_state='sample_received')
            )

        samples = list()

        for ar in result:
            ready = True
            for a in ar['Analyses']:
                if str(a['review_state']) not in ['verified', 'published']:
                    ready = False
                    break
            if ready:
                samples.append(ar)

        return samples

    def get_batches_ready_to_be_closed(self, batches=list(), also_samples=False):
        """

        :param batches:
        :param also_samples:
        :return:
        """
        # get open batches

        if len(batches) == 0:
            result = self.client.query_batches(params=dict(
                review_state='open')
            )
        else:
            result = self.client.query_batches(params=dict(
                id=[b.get('id') for b in batches],
                review_state='open')
            )

        if also_samples:
            samples = list()

        batches = list()

        for batch in result:

            ars = self.client.query_analysis_request(params=dict(
                batch_id=batch.get('id'))
            )

            ready = True
            sample = None

            for ar in ars:

                if ar.get('SampleType') in COMPLEX_SAMPLE_TYPES:
                    sample = dict(id=ar['id'], path=ar['path'])
                    continue

                if ar.get('review_state') not in ['published']:
                    ready = False
                    sample = None

                    break

            if ready:
                batches.append(batch)

                if sample and also_samples:
                    samples.append(sample)

        if also_samples:
            return batches, samples

        return batches

    def get_worksheets_ready_to_be_closed(self, worksheets=list(), also_samples=False):
        """

        :param worksheets:
        :param also_samples:
        :return:
        """
        # get open worksheets

        if len(worksheets) == 0:
            result = self.client.query_worksheets(params=dict(
                review_state='open')
            )
        else:
            result = self.client.query_worksheets(params=dict(
                id=[w.get('id') for w in worksheets],
                review_state='open')
            )

        if also_samples:
            samples = list()

        worksheets = list()

        for worksheet in result:

            ready = True
            sample = None

            for r in json.loads(worksheets.get('Remarks')):
                ars = self.client.query_analysis_request(params=dict(id=r['request_id']))
                if len(ars) == 1:
                    ar = ars.pop()
                    if ar.get('SampleType') in COMPLEX_SAMPLE_TYPES:
                        sample = dict(id=ar['id'], path=ar['path'])
                        continue

                    for a in ar.get('Analyses'):
                        if str(a['id']) == r.get('analysis_id') and\
                                        str(a['review_state']) not in ['verified','published']:

                            ready = False
                            sample = None

                            break

            if ready:
                worksheets.append(worksheet)
                if sample and also_samples:
                    samples.append(sample)

        if also_samples:
            return worksheets, samples

        return worksheets

    def close_batches(self, batches=list()):
        """

        :param batches:
        :return:
        """
        # close open batches

        if isinstance(batches, list) and len(batches) > 0:
            paths = [b.get('path') for b in batches]
            res = self.client.close_batches(paths)
            return res

        return dict()

    def close_worksheets(self, worksheets=list()):
        """

        :param worksheets:
        :return:
        """
        # close worksheets

        if isinstance(worksheets, list) and len(worksheets) > 0:
            paths = [w.get('path') for w in worksheets]
            res = self.client.close_worksheets(paths)
            return res

        return dict()

    def submit_analyses(self, analyses=list(), result='1'):
        """

        :param analyses:
        :param result:
        :return:
        """
        if isinstance(analyses, list) and len(analyses) > 0:
            paths = [a.get('path') for a in analyses]
            res = self.client.submit_analyses(paths, result)
            return res

        return dict()

    def verify_analyses(self, analyses=list()):
        """

        :param analyses:
        :return:
        """
        if isinstance(analyses, list) and len(analyses) > 0:
            paths = [a.get('path') for a in analyses]
            res = self.client.verify_analyses(paths)
            return res

        return dict()

    def publish_analyses(self, analyses=list()):
        """

        :param analyses:
        :return:
        """
        if isinstance(analyses, list) and len(analyses) > 0:
            paths = [a.get('path') for a in analyses]
            res = self.client.publish_analyses(paths)
            return res

        return dict()

    def publish_analysis_requests(self, analysis_requests=list()):
        """

        :param analysis_requests:
        :return:
        """
        # publish analysis requests
        if isinstance(analysis_requests, list) and len(analysis_requests) > 0:
            paths = [ar.get('path') for ar in analysis_requests]
            res = self.client.publish_analysis_requests(paths)
            return res

        return dict()


