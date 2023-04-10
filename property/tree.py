import rtree.index as index
import csv

class PmPoi:
    """
    POI基础数据结构
    """
    src_header = ''  # 源数据的表头

    def __init__(self):
        self.id = ''
        self.name_chn = ''
        self.addr_chn = ''
        self.alias = set()
        self.x = .0
        self.y = .0
        self.aoi_guid = ''
        self.building_guid = ''
        self.poi_type = ''
        self.freq = 1
        self.body = ''
        self.suffix = ''

    def __repr__(self):
        return "PmPoi[%s, %s, %s, %s, %f, %f]" % (self.id, self.aoi_guid, self.name_chn, self.addr_chn, self.x, self.y)
    #实例化
    @staticmethod
    def build_from_record(record):
        pm_poi = PmPoi()
        try:
            pm_poi.id = record.get('group_id')
            pm_poi.name_chn = record.get('name')
            pm_poi.addr_chn = record.get('address')
            pm_poi.x = record.get('x')
            pm_poi.y = record.get('y')
            pm_poi.poi_type = record.get('poi_type')
        except Exception as e:
            print('PmPoi: load record failed!, Error: ', e.message)
            return None
        return pm_poi
class PmPoiRtree:
    def __init__(self, poi_dict):
        rtree_index, seq_id_dict = PmPoiRtree.build_index(poi_dict)
        self.seq_id_dict = seq_id_dict
        self.rtree_index = rtree_index
        self.poi_dict = poi_dict

    @staticmethod
    def build_index(poi_dict):
        rtree_index = index.Index()
        seq_id = 0
        seq_id_dict = {}
        for poi_li in poi_dict.values():
            poi = poi_li[0]
            seq_id += 1
            delta = 1e-7
            poi_rect = Polygon(((poi.x - delta, poi.y - delta), (poi.x - delta, poi.y + delta), (poi.x + delta, poi.y + delta), (poi.x + delta, poi.y - delta), (poi.x - delta, poi.y - delta)))
            rtree_index.insert(seq_id, poi_rect.bounds)
            seq_id_dict.update({seq_id: poi.id})
        return rtree_index, seq_id_dict

    def query_poi(self, rect):
        poi_list = []
        try:
            nearby_list = list(self.rtree_index.intersection(rect))
            for seq_id in nearby_list:
                poi_id = self.seq_id_dict.get(seq_id)
                aoi_shape = self.poi_dict.get(poi_id)
                poi_list.append(aoi_shape)
        except Exception as e:
            print(e)

        return poi_list
#默认500m

    def query_poi_by_xy(self, x, y, r=0.005):
        rect = x - r, y - r, x + r, y + r
        return self.query_poi(rect)

    def load_poi_from_file(poi_path, data_type='muku'):
        poi_dict = {}
        with open(poi_path) as fs:

            rd = csv.DictReader(fs)
            print('loading poi...')
            index = 1
            for r in rd:
                if index % 5000 == 0:
                    print(' ', index)
                index += 1
                poi = None
                if data_type == 'record':
                    poi = PmPoi.build_from_record(r)
                if poi:
                    #防止主键重复导致数据被覆盖，如果主键相同只取一条可以直接根据键赋值
                    if poi_dict.get(poi.id):
                        poi_dict.get(poi.id).append(poi)
                    else:
                        poi_dict.setdefault(poi.id,[]).append(poi)
            print('load done, count: %d' % (index - 1))
        return poi_dict
