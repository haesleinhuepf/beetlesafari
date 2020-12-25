
class ClearControlDataset:

    def __init__(self, directory_name : str, dataset_name : str = 'C0opticsprefused'):
        self.directory_name = directory_name
        self.dataset_name = dataset_name

        import json
        fp = open(directory_name + "/" + dataset_name + '.metadata.txt')
        lines = fp.readlines()
        self.metadata = [json.loads(line) for line in lines]
        fp.close()

        fp = open(directory_name + "/" + dataset_name + '.index.txt')
        lines = fp.readlines()
        self.times_in_seconds = []
        self.widths = []
        self.heights = []
        self.depths = []
        for line in lines:
            elements = line.split("\t")

            self.times_in_seconds.append(float(elements[1]))

            third_element = elements[2].split(", ")
            self.widths.append(int(third_element[0]))
            self.heights.append(int(third_element[1]))
            self.depths.append(int(third_element[2]))

    def get_image(self, index = 0):
        from ..utils import index_to_clearcontrol_filename
        filename = self.directory_name + "/stacks/" + self.dataset_name + "/" + index_to_clearcontrol_filename(index)

        from ._imread_raw import imread_raw
        return imread_raw(filename, self.widths[index], self.heights[index], self.depths[index])

    def get_voxel_size_zyx(self, index):
        metadata = self.metadata[index]

        return [
            metadata['VoxelDimZ'],
            metadata['VoxelDimY'],
            metadata['VoxelDimX'],
        ]

    def get_index_after_time(self, after_time_in_seconds : float):
        for i, time in enumerate(self.times_in_seconds):
            if (time >= after_time_in_seconds):
                return i

    def get_duration_in_seconds(self):
        return self.times_in_seconds[-1]
