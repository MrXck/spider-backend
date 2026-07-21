import time
import threading


class SnowflakeIDGenerator:
    """
    雪花ID生成器
    - worker_id: 机器ID（0~1023）
    - datacenter_id: 数据中心ID（0~31）
    """

    def __init__(self, worker_id=1, datacenter_id=1):
        self.worker_id = worker_id
        self.datacenter_id = datacenter_id

        self.twepoch = 1700000000000  # 自定义起始时间戳（ms）
        self.sequence = 0
        self.sequence_bits = 12
        self.worker_id_bits = 5
        self.datacenter_id_bits = 5

        self.max_worker_id = (1 << self.worker_id_bits) - 1
        self.max_datacenter_id = (1 << self.datacenter_id_bits) - 1
        self.max_sequence = (1 << self.sequence_bits) - 1

        self.worker_id_shift = self.sequence_bits
        self.datacenter_id_shift = self.sequence_bits + self.worker_id_bits
        self.timestamp_shift = (
                self.sequence_bits + self.worker_id_bits + self.datacenter_id_bits
        )

        self.last_timestamp = -1
        self.lock = threading.Lock()

    def _gen_timestamp(self):
        return int(time.time() * 1000)

    def _til_next_millis(self, last_timestamp):
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp

    def next_id(self):
        with self.lock:
            timestamp = self._gen_timestamp()

            if timestamp < self.last_timestamp:
                raise Exception("Clock moved backwards")

            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    timestamp = self._til_next_millis(self.last_timestamp)
            else:
                self.sequence = 0

            self.last_timestamp = timestamp

            return (
                    ((timestamp - self.twepoch) << self.timestamp_shift)
                    | (self.datacenter_id << self.datacenter_id_shift)
                    | (self.worker_id << self.worker_id_shift)
                    | self.sequence
            )


snowflake = SnowflakeIDGenerator(worker_id=1, datacenter_id=1)
