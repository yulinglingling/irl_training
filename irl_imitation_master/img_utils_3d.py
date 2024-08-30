# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# def show_img(img):
#     """
#     Display a 3D image slice by slice.
#     input:
#       img: a 3D numpy array (z, y, x)
#     """
#     z_dim = img.shape[0]
#     for z in range(z_dim):
#         plt.imshow(img[z, :, :], cmap='gray')
#         plt.title(f'Slice {z}')
#         plt.colorbar()
#         plt.show()
#         input("Press Enter to continue to the next slice...")

# def heatmap2d(hm_mat, title='', block=True, fig_num=1, text=True):
#     """
#     Display 2D heatmap
#     input:
#       hm_mat:   mxn 2D np array
#     """
#     print('map shape: {}, data type: {}'.format(hm_mat.shape, hm_mat.dtype)) 

#     if block:
#         plt.figure(fig_num)
#         plt.clf()
    
#     plt.imshow(hm_mat, interpolation='nearest', cmap='hot')
#     plt.title(title)
#     plt.colorbar()
    
#     if text:
#         for y in range(hm_mat.shape[0]):
#             for x in range(hm_mat.shape[1]):
#                 plt.text(x, y, '%.1f' % hm_mat[y, x],
#                          horizontalalignment='center',
#                          verticalalignment='center')

#     if block:
#         plt.ion()
#         print('Press Enter to continue') 
#         plt.show()
#         input()

# def heatmap3d(hm_mat, title=''):
#     """
#     Display 3D heatmap
#     input:
#       hm_mat:   z x y x 3D np array
#     """
#     z_dim, y_dim, x_dim = hm_mat.shape
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     plt.title(title)

#     x, y, z = np.meshgrid(np.arange(x_dim), np.arange(y_dim), np.arange(z_dim))

#     x = x.flatten()
#     y = y.flatten()
#     z = z.flatten()
#     c = hm_mat.flatten()

#     img = ax.scatter(x, y, z, c=c, cmap='hot', marker='o')

#     plt.colorbar(img)
#     plt.show()
#     input("Press Enter to continue...")
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def show_img(img):
    """
    Display a 3D image slice by slice.
    input:
      img: a 3D numpy array (z, y, x)
    """
    z_dim = img.shape[0]
    fig, axes = plt.subplots(1, z_dim, figsize=(z_dim * 5, 5))
    if z_dim == 1:
        axes = [axes]
    for z in range(z_dim):
        axes[z].imshow(img[z, :, :], cmap='gray')
        axes[z].set_title(f'Slice {z}')
        axes[z].axis('off')
    plt.show()

def heatmap2d(ax, hm_mat, title='', text=True):
    """
    Display 2D heatmap on the given Axes object.
    input:
      ax:       Axes object
      hm_mat:   mxn 2D np array
      title:    Title for the plot
      text:     Whether to display text annotations
    """
    print('map shape: {}, data type: {}'.format(hm_mat.shape, hm_mat.dtype)) 

    ax.clear()
    im = ax.imshow(hm_mat, interpolation='nearest', cmap='hot')
    ax.set_title(title)
    plt.colorbar(im, ax=ax)
    
    if text:
        for y in range(hm_mat.shape[0]):
            for x in range(hm_mat.shape[1]):
                ax.text(x, y, '%.1f' % hm_mat[y, x],
                        horizontalalignment='center',
                        verticalalignment='center')

# def heatmap3d(ax, hm_mat, title=''):
#     """
#     Display 3D heatmap on the given Axes3D object.
#     input:
#       ax:       Axes3D object
#       hm_mat:   z x y x 3D np array
#       title:    Title for the plot
#     """
#     z_dim, y_dim, x_dim = hm_mat.shape
#     ax.clear()
#     ax.set_title(title)
#     ax.set_xlabel('X')
#     ax.set_ylabel('Y')
#     ax.set_zlabel('Z')

#     x, y, z = np.meshgrid(np.arange(x_dim), np.arange(y_dim), np.arange(z_dim))
#     x = x.flatten()
#     y = y.flatten()
#     z = z.flatten()
#     c = hm_mat.flatten()

#     img = ax.scatter(x, y, z, c=c, cmap='hot', marker='o')
#         # Invert y-axis direction
#     ax.set_ylim([y_dim, 0])  # Invert the y-axis range
#     plt.colorbar(img, ax=ax)
def heatmap3d(ax, hm_mat, title=''):
    """
    Display 3D heatmap on the given Axes3D object.
    input:
      ax:       Axes3D object
      hm_mat:   z x y x 3D np array
      title:    Title for the plot
    """
    z_dim, y_dim, x_dim = np.array(hm_mat).shape
    ax.clear()
    ax.set_title(title)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Generate meshgrid
    x, y, z = np.meshgrid(np.arange(x_dim), np.arange(y_dim), np.arange(z_dim))
    x = x.flatten()
    y = y.flatten()
    z = z.flatten()
    c = np.array(hm_mat).flatten(order = 'F')
    # print("x", x);
    # print("y", y)
    # print("c", c)

    # Scatter plot
    img = ax.scatter(x, y, z, c=c, cmap='hot', marker='o')

    # Invert y-axis direction
    # ax.set_ylim([y_dim, 0])  # Invert the y-axis range

    # Add colorbar
    plt.colorbar(img, ax=ax)

    # Display value at each point
    for i in range(len(x)):
        ax.text(x[i], y[i], z[i], f'{c[i]:.1f}', color='black', fontsize=8, ha='center', va='center')

    # Optional: Adjust the view angle for better visibility of text
    ax.view_init(elev=30, azim=45)


def main():
    # Example 3D data
    z_dim, y_dim, x_dim = 4, 5, 6
    data = np.random.rand(z_dim, y_dim, x_dim)

    fig = plt.figure(figsize=(20, 12))

    # Display 2D slices
    ax1 = fig.add_subplot(2, 2, 1)
    show_img(data)  # Will create individual slices

    # Display 2D heatmap (example)
    ax2 = fig.add_subplot(2, 2, 2)
    heatmap2d(ax2, np.mean(data, axis=0), '2D Heatmap')

    # Display 3D heatmap (example)
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    heatmap3d(ax3, data, '3D Heatmap')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()
