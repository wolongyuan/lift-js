from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt

with PdfPages('out.pdf') as pdf:
    optimized, = plt.plot([100,200,300,400,500,600,700,800,900], [0.376441001892, 0.698533773422, 1.04884314537, 1.38629603386, 1.75367999077, 1.93270492554, 2.15085792542, 2.38690686226, 2.55937290192])
    baseline, = plt.plot([500, 850], [1.75367999077, 3], 'b--')
    plt.xlabel('Number of iteration')
    plt.ylabel('Execution time')
    plt.legend([baseline, optimized], ["baseline", "optimized "], loc=4)
    pdf.savefig()
    plt.close()
