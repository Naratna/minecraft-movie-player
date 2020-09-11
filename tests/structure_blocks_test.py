import unittest
from context import structure_block

class StructureBlocksTest(unittest.TestCase):

    redstone = "minecraft:redstone_block"
    dirt = "minecraft:dirt"
    stone = "minecraft:stone"
    
    def setUp(self):
        self._sizes = (20,20,20)
        self._structure = structure_block.StructureBlock(self._sizes)

    def test_size(self):
        
        size = self._structure._size
        self.assertTupleEqual((size[0], size[1], size[2]),self._sizes)

    def test_setblock(self):
        inputs = [
            ((10,10,10), self.stone),
            ((19,12,13), self.dirt),
            ((8,5,7), "minecraft:air"),
            ((10,10,10), self.stone),
            ((10,10,11), self.stone),
            ((10,11,10), "minecraft:air"),
            ((11,10,10), self.dirt),
        ]
        for coordinates, block_id in inputs:
            x, y , z = coordinates
            self._structure.setblock(coordinates,block_id)
            self.assertTrue(block_id in self._structure._palette)
            self.assertEqual(self._structure._blocks[x][y][z], self._structure._palette[block_id])

    def test_save_file(self):
        blocks = [
            ((0,0,0),self.redstone),
            ((0,0,1),self.redstone),
            ((0,0,2),self.redstone),
            ((0,0,1),self.redstone),
            ((0,1,0),self.stone),
            ((0,1,1),self.stone),
            ((0,1,2),self.stone),
            ((0,1,3),self.stone),
            ((0,2,0),self.dirt),
            ((0,2,1),self.dirt),
            ((0,2,2),self.dirt),
            ((0,2,3),self.dirt),
        ]
        for coordinates, block_id in blocks:
            self._structure.setblock(coordinates, block_id)
        self._structure.save("D:\\Desarrollo\\Python\\minecraft-movie-player\\test-io\\nbt-test.nbt")


if __name__ == "__main__":
    unittest.main()

