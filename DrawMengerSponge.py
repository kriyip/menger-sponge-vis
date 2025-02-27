# Creates an interactive 3D plot of a Menger sponge with the specified recursion depth
# Call with python DrawMengerSponge.py <depth>
# e.g. python DrawMengerSponge.py 3

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import sys
def draw_cube(ax, origin, size, color='black', edgecolor='white', alpha=0.75):
    """
    Draw a cube with lower–left–front corner at 'origin' and side length 'size'

    Parameters:
      ax     -- a matplotlib 3D axis
      origin -- the (x, y, z) coordinates of the current cube's origin (lower–left–front corner)
      size   -- the side length
      color  -- the color of the cube
      edgecolor -- the color of the cube's edges
      alpha  -- the transparency of the cube
    """
    x, y, z = origin

    # define the 8 corners of the cube.
    vertices = [
        (x,         y,         z),
        (x + size,  y,         z),
        (x + size,  y + size,  z),
        (x,         y + size,  z),
        (x,         y,         z + size),
        (x + size,  y,         z + size),
        (x + size,  y + size,  z + size),
        (x,         y + size,  z + size)
    ]
    
    # can define the 6 faces of the cube as lists of vertices.
    faces = [
        [vertices[0], vertices[1], vertices[2], vertices[3]],  # bottom
        [vertices[4], vertices[5], vertices[6], vertices[7]],  # top
        [vertices[0], vertices[1], vertices[5], vertices[4]],  # front
        [vertices[2], vertices[3], vertices[7], vertices[6]],  # back
        [vertices[1], vertices[2], vertices[6], vertices[5]],  # right
        [vertices[0], vertices[3], vertices[7], vertices[4]]   # left
    ]
    
    # creates 3D cube from the faces
    poly3d = Poly3DCollection(faces, facecolors=color, edgecolors=edgecolor, linewidths=0.5, alpha=alpha)
    
    # add the cube to the plot
    ax.add_collection3d(poly3d)

def menger(ax, origin, size, depth):
    """
    Recursively draw the Menger sponge
    Keeps only subcubes with at most one of the indices being 1
        (1,1,0), (1,1,1), (1,1,2), (1,0,1), (1,2,1), (0,1,1), (2,1,1)

    Parameters:
      ax     -- a matplotlib 3D axis
      origin -- the (x, y, z) coordinates of the current cube's origin (lower–left–front corner)
      size   -- the side length of the current cube
      depth  -- recursion depth; if 0, draw the cube, otherwise subdivide.
    """
    if depth == 0:
        # base case: draw current cube
        draw_cube(ax, origin, size)
    else:
        new_size = size / 3.0
        
        # loop over the 27 subcubes
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    # Only keep the subcube if at most one of the indices is 1
                    if [i, j, k].count(1) <= 1:
                        new_origin = (origin[0] + i * new_size,
                                      origin[1] + j * new_size,
                                      origin[2] + k * new_size)
                        # Recursively draw the subcube (easier than removing invalid subcubes)
                        menger(ax, new_origin, new_size, depth - 1)

if __name__ == '__main__':
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    if len(sys.argv) != 2:
        print("Usage: python DrawMengerSponge.py <depth>")
        sys.exit(1)
    if not sys.argv[1].isdigit():
        print("Depth must be an integer")
        sys.exit(1)
    
    recursion_depth = int(sys.argv[1])
    menger(ax, (0, 0, 0), 1.0, recursion_depth)
    
    # make plot look better
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Menger Sponge (depth = {recursion_depth})')
    
    # make isometric view
    ax.view_init(elev=20, azim=30)
    
    plt.show()
