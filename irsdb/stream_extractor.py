import unicodecsv as csv
from irsx.xmlrunner import XMLRunner


class StreamExtractor(object):
    """Write filings to csv, specified in config.py"""

    def __init__(self, output_streams, data_capture_dict):
        self.output_streams = output_streams
        self.data_capture_dict = data_capture_dict
        self.xml_runner = XMLRunner()
        self._init_streams()


    def _init_streams(self):
        for stream_key in self.output_streams.keys():
            this_stream = self.output_streams[stream_key]
            filename = this_stream['filename']  + ".csv"
            print("Initializing output stream %s" % filename)
            outfile = open(filename , 'wb')
            dw = csv.DictWriter(outfile, this_stream['headers'], extrasaction='ignore')
            dw.writeheader()
            self.output_streams[stream_key]['writer'] = dw



    def run_parts(self, this_capture_sked, parsed_sked, sked, taxpayer_name=""):
        #print("run parts %s \n %s " % (this_capture_sked, parsed_sked) )
        for part_key in this_capture_sked['parts'].keys():
            stream_key = this_capture_sked['parts'][part_key]['stream_key']
            this_stream = self.output_streams[stream_key]
            part = None
            try:
                part = parsed_sked['schedule_parts'][part_key]
            except KeyError:
                continue

            capture_dict = this_capture_sked['parts'][part_key]

            row_data = {}
            row_data['form'] = sked
            row_data['source'] = part_key
            row_data['taxpayer_name'] = taxpayer_name


            for capture_key in capture_dict.keys():
                if capture_key == 'stream_key':
                    continue
                try:
                    val = part[capture_key]
                    csv_header = capture_dict[capture_key]['header']
                    row_data[csv_header] = val

                except KeyError:
                    try:
                        default = capture_dict[capture_key]['default']
                        csv_header = capture_dict[capture_key]['header']
                        row_data[csv_header]=default
                    except KeyError:
                        #print("Key Error %s" % capture_key)
                        pass

            ## Composite keys: Not implemented here. 

            #print("row data is %s" % row_data)
            ## We've gone through who whole part -- write it to file
            this_stream['writer'].writerow(row_data)



    def run_groups(self, this_capture_sked, parsed_sked, sked, taxpayer_name=""):
        for group_key in this_capture_sked['groups'].keys():
            stream_key = this_capture_sked['groups'][group_key]['stream_key']
            this_stream = self.output_streams[stream_key]
            groups = None
            try:
                groups = parsed_sked['groups'][group_key]
            except KeyError:
                #print("No groups found for %s\n" % group_key)
                continue

            for group in groups:
                capture_dict = this_capture_sked['groups'][group_key]
                row_data = {}
                row_data['form'] = sked
                row_data['source'] = group_key
                row_data['taxpayer_name'] = taxpayer_name

                for capture_key in capture_dict.keys():
                    if capture_key == 'stream_key':
                        continue
                    try:
                        val = group[capture_key]
                        csv_header = capture_dict[capture_key]['header']
                        row_data[csv_header] = val

                    except KeyError:
                        try:
                            default = capture_dict[capture_key]['default']
                            csv_header = capture_dict[capture_key]['header']
                            row_data[csv_header]=default
                        except KeyError:
                            pass

                ## now look for "composite keys"
                composite_groups = None
                try:
                    composite_groups = capture_dict['composite']
                except KeyError:
                    pass

                # composite groups are summed up from existing vars, and need a default
                if composite_groups:
                    for composite_group_key in composite_groups.keys():
                        total = 0
                        for cg_part in composite_groups[composite_group_key].keys():
                            try:
                                val = group[cg_part]
                                total += int(val)
                            except KeyError:
                                total += composite_groups[composite_group_key][cg_part]['default']
                        row_data[composite_group_key] = total

                ## We've gone through who whole group -- write it to file
                this_stream['writer'].writerow(row_data)

    def run_filing(self, filing, taxpayer_name=""):

        parsed_filing = self.xml_runner.run_filing(filing)
        schedule_list = parsed_filing.list_schedules()

        if ( int(parsed_filing.get_version()[:4]) < 2013 ):
            print("Skipping pre-2013 schemas")
            return None

        for sked in self.data_capture_dict.keys():
            if sked in schedule_list:
                #print ("Running sked %s" % sked)
                parsed_skeds = parsed_filing.get_parsed_sked(sked)
                if parsed_skeds:
                    parsed_sked = parsed_skeds[0]
                else:
                    continue
        
                this_capture_sked = self.data_capture_dict[sked]
            

                ### Repeating Groups 
                skip_groups = False
                try:
                     this_capture_sked['groups']
                except KeyError:
                     skip_groups = True
                if not skip_groups:
                    self.run_groups(this_capture_sked, parsed_sked, sked, taxpayer_name=taxpayer_name)


                ### Nonrepeating schedule parts 
                skip_parts = False
                try:
                     this_capture_sked['parts']
                except KeyError:
                     skip_parts = True
                if not skip_parts:
                    self.run_parts(this_capture_sked, parsed_sked, sked, taxpayer_name=taxpayer_name)
            else:
                #print("missing sked %s" % sked)
                pass

                
