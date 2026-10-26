import unittest

from support import frame, jitter
from f0converter.errors import ConvertError
from f0converter.signal.cluster import clean_codes, cluster_values
from f0converter.signal.frames import extract_frame, median, similar, split_frames


class ClusterTest(unittest.TestCase):
    def test_groups_take_the_most_frequent_value(self):
        mapping = cluster_values([300, 300, 300, 290, 310, 900, 905, 905, 1200], 0.25)
        self.assertEqual(mapping, {290: 300, 300: 300, 310: 300, 900: 905, 905: 905, 1200: 1200})

    def test_pulses_and_pauses_separately_over_all_codes(self):
        codes = clean_codes([[300, 302, 302, 9000], [302, 302, 302, 9100]], 0.25)
        self.assertEqual(codes, [[302, 302, 302, 9000], [302, 302, 302, 9000]])


class FramesTest(unittest.TestCase):
    def test_split_frames(self):
        self.assertEqual(split_frames([1, 2, 3, 6000, 4, 5, 6], 5000),
                         [([1, 2, 3, 6000], True), ([4, 5, 6], False)])
        self.assertEqual(split_frames([1, 6000], 5000), [([1, 6000], True)])

    def test_similar_ignores_the_last_pause(self):
        first = frame("1010")
        self.assertTrue(similar(first, first[:-1] + [20000], 0.25))
        self.assertTrue(similar(first, [value + 100 for value in first], 0.0))
        self.assertFalse(similar(first, [first[0] + 400] + first[1:], 0.25))
        self.assertFalse(similar(first, first[:-2], 0.25))

    def test_median(self):
        self.assertEqual(median([5, 1, 3]), 3)
        self.assertEqual(median([4, 1, 3, 2]), 3)

    def test_extract_frame_from_repeats(self):
        expected = frame("110010100111")
        noise = [140, 90, 210, 6000]
        values = noise + sum((jitter(expected, offset) for offset in range(4)), []) + expected[:9]
        result, description = extract_frame(values, 5000, 0.25)
        self.assertEqual(result, expected)
        self.assertEqual(description, "4 of 6 frames match")

    def test_single_frame(self):
        expected = frame("110010100111")
        self.assertEqual(extract_frame(expected, 5000, 0.25), (expected, "single frame taken as is"))

    def test_errors(self):
        with self.assertRaisesRegex(ConvertError, "noise only"):
            extract_frame([300, 900] * 20, 5000, 0.25)
        with self.assertRaisesRegex(ConvertError, "no frame repeats in 2 frames"):
            extract_frame(frame("110010100111") + frame("000000000000") + [300], 5000, 0.25)


if __name__ == "__main__":
    unittest.main()
