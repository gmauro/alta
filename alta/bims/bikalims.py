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
        self.log.info("{}".format(self.client.version))
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

    def get_batch_info(self, batch_label, sample_list=list()):
        """
        Given a valid bika batch label, returns a dictionary filled with all
        the info of the samples owned by the batch

        :type batch_label: str
        :param batch_label:
        :param sample_list:
        :return: a dictionary with as key the sample id and value a
        dictionary collecting the type, label and external label of the sample
        """
        result = self.client.query_analysis_request(params=dict(
            batch_id=batch_label)
        )

        if result:
            batch_info = dict()
            for r in result:
                if len(sample_list) > 0 and r['id'] not in sample_list:
                    continue

                analyses = {}
                for a in r['Analyses']:
                    analyses[a['Title']] = a['review_state']

                sub_d = {'type': r['SampleTypeTitle'],
                         'sample_label': r['Title'],
                         'client_sample_id': r['ClientSampleID'],
                         'runs': r['Sampler'],
                         'request_id': r['id'],
                         'analyses': analyses
                         }
                batch_info[r['SampleID']] = sub_d
            return batch_info
        else:
            return None

    def get_run_info(self, run_label):
        """
        Given a valid rundir label, returns a dictionary filled with all
        the info of the samples owned by the runs

        :type run_label: str
        :param run_label:
        :return: a dictionary with as key the sample id and value a
        dictionary collecting the type, label and external label of the sample
        """
        result = self.client.query_analysis_request(params=dict(
            run=run_label)
        )

        if result:
            run_info = dict()
            for r in result:
                analyses = {}
                for a in r['Analyses']:
                    analyses[a['Title']] = a['review_state']

                sub_d = {'type': r['SampleTypeTitle'],
                         'sample_label': r['Title'],
                         'client_sample_id': r['ClientSampleID'],
                         'runs': r['Sampler'],
                         'request_id': r['id'],
                         'analyses': analyses
                         }
                run_info[r['id']] = sub_d
            return run_info
        else:
            return None

    def get_analysis_request_by_service(self, analysis_service_id=None, review_state='published'):
        result = self.client.query_analysis_request(params=dict(
            analysis_service_id=analysis_service_id,
            review_state=review_state)
        )

        if result:
            res = [dict(
                id=str(r['id']),
                title=str(r['Title']),
                sample_id=str(r['SampleID']),
                sample_type=str(r['SampleTypeTitle']),
                path=str(r['path']),
                client_sample_id=str(r['ClientSampleID']),
                client=str(r['Client']),
                contact=str(r['Contact']),
                cccontact=[str(c) for c in r['CCContact']],
                batch_id=str(r['title']),
                batch_title=str(r['Batch']),
                date=str(r['Date']),
                date_received=str(r['DateReceived']),
                date_published=str(r['DatePublished']),
                date_created=str(r['creation_date']),
                review_state=str(r['review_state']) if 'published' in str(
                    r['review_state']) else str(r['subject'][0]),
                remarks=str(r['Remarks']),
                rights=str(r['rights']),
                results_interpretation=str(r['ResultsInterpretation']),
                params=self._get_environmental_conditions(r['EnvironmentalConditions']),
                creator=str(r['Creator']),
                analyses=self._get_analyses(r['Analyses']),
                runs=self._get_runs_ar(r['Sampler']),
                transitions=[dict(id=str(t['id']), title=str(t['title'])) for t in r['transitions']],
            ) for r in result
                if len(self.client.query_batches(params=dict(
                    id=str(r['title']),
                    review_state='cancelled'))) == 0]

            return res

        return list()

    def get_analyses_ready_to_be_synchronized(self, samples=list(), action='submit', sync_all_analyses=False):
        """
        Given a list of bika Analysis Requests object, returns their analyses ready to be synchronized
        if no list is given, returns ALL analyses ready to be synchronized
        :param samples:
        :param action:
        :param sync_all_analyses:
        :return: a list of bika Analyses object
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
            result = self.client.query_analysis_request(params=dict(
                review_state='sample_received')
            )
        else:
            result = self.client.query_analysis_request(params=dict(
                id=[s.get('id') for s in samples],
                review_state='sample_received')
            )

        analyses = list()

        for ar in result:
            for a in ar['Analyses']:
                if (str(a['Keyword']) not in ANALYSIS_NOT_SYNC or sync_all_analyses) \
                        and str(a['review_state']) == get_review_state(action):
                    path = os.path.join(ar['path'], a['id'])
                    a.update(dict(path=path))
                    analyses.append(a)

        return analyses

    def get_analysis_requests_ready_to_be_published(self, samples=list()):
        """
        Given a list of bika Analysis Requests object, returns the ones ready to be published
        if no list is given, returns ALL analysis requests ready to be published
        :param samples:
        :return: a list of bika Analysis Request object
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

        this_samples = list()

        for ar in result:
            ready = True
            for a in ar['Analyses']:
                if str(a['review_state']) not in ['verified', 'published']:
                    ready = False
                    break
            if ready:
                this_samples.append(ar)

        return this_samples

    def get_batches_ready_to_be_closed(self, batches=list(), also_samples=False):
        """
        Given a list of bika Batches object, returns the ones ready to be closed
        if no list is given, returns ALL batches ready to be closed
        :param batches:
        :param also_samples:
        :return: a list of bika Batches object
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
            this_samples = list()

        this_batches = list()

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
                this_batches.append(batch)

                if sample and also_samples:
                    this_samples.append(sample)

        if also_samples:
            return this_batches, this_samples

        return this_batches

    def get_delivery_info(self, delivery_id, review_state='all'):
        """
        Given a valid bika delivery id, returns a dictionary filled with all
        the info

        :type delivery_id: str
        :param delivery_id:

        :return: a dictionary with as key the sample id and value a
        dictionary collecting the type, label and external label of the sample
        """
        result = self.client.query_deliveries(params=dict(
            id=delivery_id,
            review_state=review_state)
        )
        if result and isinstance(result, list) and len(result) == 1:
            delivery = self._get_deliveries(result)[0]
            samples_info = dict()
            for sample_id in delivery.get('samples'):
                ar = self.client.query_analysis_request(params=dict(id=sample_id))[0]

                samples_info[ar['SampleID']] = dict(
                    type=ar['SampleTypeTitle'],
                    sample_label=ar['Title'],
                    client_sample_id=ar['ClientSampleID'],
                    runs=ar['Sampler'],
                    request_id=ar['id'],
                    batch_id=ar['title'],
                )
            delivery['samples_info'] = samples_info
            return delivery
        else:
            return None

    def get_deliveries_ready_to_process(self, deliveries=list()):
        """
        Given a list of bika Deliveries object, returns the ones ready to be processed
        if no list is given, returns ALL deliveries ready to be processed
        :param deliveries:
        :return: a list of bika Worksheets object
        """
        # get open worksheets

        if len(deliveries) == 0:
            result = self.client.query_deliveries(params=dict(
                review_state='ready')
            )
        else:
            result = self.client.query_deliveries(params=dict(
                id=[d.get('id') for d in deliveries],
                review_state='ready')
            )

        return self._get_deliveries(result)

    def get_worksheets_ready_to_be_closed(self, worksheets=list(), also_samples=False):
        """
        Given a list of bika Worksheets object, returns the ones ready to be closed
        if no list is given, returns ALL worksheets ready to be closed
        :param worksheets:
        :param also_samples:
        :return: a list of bika Worksheets object
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
            this_samples = list()

        this_worksheets = list()

        for worksheet in result:

            ready = True
            sample = None

            for r in json.loads(worksheet.get('Remarks')):
                ars = self.client.query_analysis_request(params=dict(id=r['request_id']))
                if len(ars) == 1:
                    ar = ars.pop()
                    if ar.get('SampleType') in COMPLEX_SAMPLE_TYPES:
                        sample = dict(id=ar['id'], path=ar['path'])
                        continue

                    for a in ar.get('Analyses'):
                        if str(a['id']) == r.get('analysis_id') and \
                                        str(a['review_state']) not in ['verified', 'published']:
                            ready = False
                            sample = None

                            break

            if ready:
                this_worksheets.append(worksheet)
                if sample and also_samples:
                    this_samples.append(sample)

        if also_samples:
            return this_worksheets, this_samples

        return this_worksheets

    def close_batches(self, batches=list()):
        """
        Given a list of bika Batches object, close them
        :param batches:
        :return: response dict from bika
        """
        # close open batches

        if isinstance(batches, list) and len(batches) > 0:
            paths = [b.get('path') for b in batches]
            res = self.client.close_batches(paths)
            return res

        return dict()

    def close_worksheets(self, worksheets=list()):
        """
        Given a list of bika Worksheets object, close them
        :param worksheets:
        :return: response dict from bika
        """
        # close worksheets

        if isinstance(worksheets, list) and len(worksheets) > 0:
            paths = [w.get('path') for w in worksheets]
            res = self.client.close_worksheets(paths)
            return res

        return dict()

    def submit_analyses(self, analyses=list(), result='1'):
        """
        Given a list of bika Analyses object, submit them
        :param analyses:
        :param result:
        :return: response dict from bika
        """
        if isinstance(analyses, list) and len(analyses) > 0:
            paths = [a.get('path') for a in analyses]
            res = self.client.submit_analyses(paths, result)
            return res

        return dict()

    def verify_analyses(self, analyses=list()):
        """
        Given a list of bika Analyses object, verify them
        :param analyses:
        :return: response dict from bika
        """
        if isinstance(analyses, list) and len(analyses) > 0:
            paths = [a.get('path') for a in analyses]
            res = self.client.verify_analyses(paths)
            return res

        return dict()

    def publish_analyses(self, analyses=list()):
        """
        Given a list of bika Analyses object, publish them
        :param analyses:
        :return: response dict from bika
        """
        if isinstance(analyses, list) and len(analyses) > 0:
            paths = [a.get('path') for a in analyses]
            res = self.client.publish_analyses(paths)
            return res

        return dict()

    def publish_analysis_requests(self, analysis_requests=list()):
        """
        Given a list of bika Analysis Request object, submit them
        :param analysis_requests:
        :return: response dict from bika
        """
        # publish analysis requests
        if isinstance(analysis_requests, list) and len(analysis_requests) > 0:
            paths = [ar.get('path') for ar in analysis_requests]
            res = self.client.publish_analysis_requests(paths)
            return res

        return dict()

    def set_delivery_started(self, delivery_id):
        """
        Given a bika Delivery object, set it as processing
        :param delivery_id:
        :return: response dict from bika
        """
        # set delivery as processing
        result = self.client.query_deliveries(params=dict(
            id=delivery_id,
            review_state='ready')
        )

        if result and isinstance(result, list) and len(result) == 1:
            delivery = self._get_deliveries(result)[0]

            if delivery and isinstance(delivery, dict) and len(delivery) > 0:
                path = delivery.get('path')
                res = self.client.set_delivery_started(path)
                return res

        return dict()

    def set_delivery_completed(self, delivery_id):
        """
        Given a bika Delivery object, set it as delivered
        :param delivery_id:
        :return: response dict from bika
        """
        # set delivery as processing
        result = self.client.query_deliveries(params=dict(
            id=delivery_id,
            review_state='processing')
        )

        if result and isinstance(result, list) and len(result) == 1:
            delivery = self._get_deliveries(result)[0]

            if delivery and isinstance(delivery, dict) and len(delivery) > 0:
                path = delivery.get('path')
                res = self.client.set_delivery_completed(path)
                return res

        return dict()

    def update_delivery_details(self, delivery_id, user=None, password=None, path=None):

        result = self.client.query_deliveries(params=dict(
            id=delivery_id)
        )

        if result and isinstance(result, list) and len(result) == 1:
            delivery = self._get_deliveries(result)[0]
            obj_path = delivery.get('path')
            details = delivery.get('details')

            details['user'] = user if user else details['user']
            details['password'] = password if password else details['password']
            details['path'] = path if path else details['path']

            res = self.client.update_delivery_details(obj_path, details)
            return res

        return dict()

    def _get_analyses(self, analyses):
        return [dict(
            id=str(r['id']),
            title=str(r['Title']),
            description=str(r['description']),
            keyword=str(r['Keyword']),
            category=str(r['CategoryTitle']),
            result=str(r['Result']),
            client=str(r['ClientTitle']),
            due_date=str(r['DueDate']),
            date_received=str(r['DateReceived']),
            date_sampled=str(r['DateSampled']),
            date_pubblished=str(r['DateAnalysisPublished']),
            result_date=str(r['ResultCaptureDate']),
            analyst=str(r['Analyst']),
            request_id=str(r['RequestID']),
            review_state=str(r['review_state']),
            remarks=str(r['Remarks']),
            uid=str(r['UID']),
            transitions=[dict(id=str(t['id']), title=str(t['title'])) for t in r['transitions']],
        ) for r in analyses]

    def _get_deliveries(self, deliveries):
        return [dict(
            id=r.get('id'),
            title=r.get('title'),
            description=r.get('description'),
            path=r.get('path'),
            details=json.loads(r.get('location')),
            creation_date=r.get('creation_date'),
            modification_date=r.get('modification_date'),
            date=r.get('Date'),
            samples=[s.get('request_id') for s in json.loads(r.get('Remarks'))],
            review_state=r.get('subject')[0] if len(r.get('subject')) == 1 else '',
            uid=r.get('UID'),
            creator=r.get('Creator'),

        ) for r in deliveries]

    def _get_service_data(self, analysis_services_settings):
        for settings in analysis_services_settings:
            if 'service_data' in settings:
                services_data = [dict(
                    id=str(s['id']),
                    title=str(s['Title']),
                    price=str(s['Price']),
                    path=str(s['path']),
                ) for s in settings['service_data']]
                return services_data
        return []

    def _get_environmental_conditions(self, str_environmental_conditions):
        environmental_conditions = list()
        if '=' in str_environmental_conditions:
            for ec in str_environmental_conditions.split('|'):
                items = ec.split('=')
                if len(items) == 2:
                    environmental_conditions.append(dict(label=str(items[0]), value=str(items[1])))
        elif len(str_environmental_conditions.strip()) > 0:
            for evc in json.loads(str_environmental_conditions):
                for k, v in evc.iteritems():
                    environmental_conditions.append(dict(label=str(k), value=str(v)))

        return environmental_conditions

    def _get_runs_ar(self, str_runs):
        runs = list()
        if isinstance(str_runs, list):
            return str_runs
        elif len(str_runs.strip()) > 0:
            return json.loads(str_runs)
        return runs
