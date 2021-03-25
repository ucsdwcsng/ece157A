#!/usr/bin/env python
# coding: utf-8

# Importing all the libraries:

# In[4]:


get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plt
import numpy as np
import scipy as scp


# Testing functions

# In[5]:


t = np.arange(0,1.0,0.001); # Sampling time instants
x_of_t = np.sin(2*np.pi*1*t);

plt.plot(t,x_of_t)
plt.xlabel('Time (s)')
plt.ylabel('Sample Value - x[n]')

plt.show()


# Reading Samples From a File

# In[34]:


filename = "filename.dat"
f_sig = np.fromfile(open(filename), dtype=np.complex64)


# In[43]:


# Plotting the Real and Imaginary Parts (time domain)
# of the received samples
plt.plot(np.real(f_sig[90:610]))
plt.plot(np.imag(f_sig[90:610]))
plt.show()


# In[47]:


# Plotting the Frequency Domain
nfft = 1024;
freq_sig = np.fft.fftshift(np.fft.fft(f_sig,nfft));

plt.plot(np.abs(freq_sig))
plt.show()

