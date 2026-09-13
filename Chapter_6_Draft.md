# Chapter 6: Conclusion

## 6.1 Conclusion
The exponential proliferation of digital data has fundamentally destabilized traditional law enforcement triage workflows. Digital forensic investigators are routinely tasked with identifying explicit or illicit materials buried within terabyte-sized hard drives containing hundreds of thousands of benign images. This dissertation sought to address the severe operational limitations of both traditional cryptographic hash-matching (which is rendered obsolete by minor file alterations) and modern Deep Learning architectures (which demand prohibitive graphical computing hardware unavailable to standard field units). 

The core hypothesis of this research proposed that a return to explicitly defined, mathematically deterministic classical computer vision techniques—specifically utilizing the Histogram of Oriented Gradients (HOG) and 3D HSV Color Histograms—could achieve legally defensible triage accuracy while operating at a fraction of the computational latency of neural networks.

The empirical findings of this study robustly validate this hypothesis. By engineering a custom, real-world forensic dataset comprising Drugs, Alcohol, and Weapons, the engineered classical Support Vector Machine (SVM) pipeline successfully achieved an overall statistical accuracy of 88.4%. Most importantly, the classical pipeline maintained an impressive Recall rate of 86.1%, effectively minimizing catastrophic false negatives where critical evidence is missed. 

When benchmarked against fine-tuned deep learning architectures, deep models like ResNet-50 achieved higher raw accuracy (99.50% vs 88.4%). However, the CPU inference latency benchmark revealed the stark operational reality: the classical SVM processed a single image in just ~96.52 milliseconds on a standard Intel CPU, whereas ResNet-50 required 294.22 milliseconds (over 3× longer), and VGG-16 required 512.40 milliseconds (over 5.3× longer). In a practical deployment scenario involving the rapid triage of 500,000 seized images on standard field hardware, the classical SVM pipeline completes the operation in approximately 13.4 hours (readily accomplished during an overnight run), whereas ResNet-50 would require approximately 40.8 hours (~1.7 days) and VGG-16 over 71 hours (~3 days) of continuous processing. This substantial processing discrepancy confirms that classical algorithms remain not only viable but pragmatic and necessary for frontline investigative work where time and hardware resources are severely constrained.

Furthermore, this research successfully demonstrated the integration of a Semantic Optical Character Recognition (OCR) safety net. By forcing the system to explicitly read the physical labels on identified objects (e.g., extracting the word "Prescription" from a bottle), the hybrid pipeline successfully bypassed the inherent visual bias of purely geometric classifiers. This synthesis of classical speed and semantic intelligence yields an explainable, transparent, and legally robust tool that directly resolves the "black-box" legal criticisms currently plaguing deep learning deployments in criminal courts.

### 6.1.1 The Socioeconomic Impact of Rapid Triage
Beyond the strict computational and legal metrics, the success of the classical hybrid pipeline carries profound socioeconomic implications for the criminal justice system. Across the United Kingdom and internationally, forensic laboratories are facing critical backlogs, with devices frequently waiting up to 18 months to be analyzed. This severe delay inherently violates the rights of defendants awaiting trial and prevents investigators from rapidly securing convictions in high-risk cases. By reducing the triage time from over 40 hours down to just ~13.4 hours on standard CPU hardware (and dramatically outperforming unoptimized legacy architectures), law enforcement agencies can effectively alleviate these backlogs without requiring massive injections of municipal funding to purchase proprietary GPU clusters. 

Furthermore, the automation of the initial triage phase drastically reduces the psychological burden placed on human analysts. Forcing human investigators to manually scroll through terabytes of potentially disturbing imagery inevitably leads to severe cognitive fatigue and documented cases of Post-Traumatic Stress Disorder (PTSD). By utilizing a mathematically robust SVM to automatically filter the benign background noise, human analysts are only exposed to the explicit subset of flagged evidence, fundamentally improving the occupational health and safety standards within modern digital forensic units.

## 6.2 Future Work
While the deterministic hybrid pipeline engineered in this study represents a significant leap forward in pragmatic forensic triage, the rapid evolution of cybercrime and digital forensics necessitates continuous technological advancement. Several highly promising avenues for future research and development have been identified to further enhance the system's operational deployment.

### 6.2.1 Edge-Device and Mobile Deployment
The low mathematical overhead of the HOG-SVM pipeline presents a unique opportunity for extreme edge-device deployment. Future iterations of this project should explore porting the OpenCV pipeline from standard investigative laptops directly onto the issued smartphones of frontline police officers. By optimizing the C++ backend of OpenCV for ARM architectures, field officers could theoretically perform real-time visual triage of a suspect's device directly at the crime scene, completely bypassing the need to seize and transport the device back to a centralized forensic laboratory. This would drastically accelerate the initial intelligence-gathering phase of a criminal investigation.

### 6.2.2 Federated Learning for Cross-Jurisdictional Intelligence
A persistent constraint in digital forensic machine learning is the inability to legally share datasets between different national or international law enforcement agencies due to strict privacy and data protection laws (such as GDPR in Europe or HIPAA in the United States). Future work should rigorously explore the implementation of Federated Learning protocols. Federated Learning allows multiple disconnected forensic laboratories to collaboratively train a shared global model without ever transferring or exposing the underlying private evidence. By periodically sharing only the encrypted mathematical weight updates of the SVM or Random Forest algorithms, international agencies could collectively combat evolving illicit visual trends (such as new branding on narcotic packaging) while maintaining strict legal compliance.

### 6.2.3 Advancements in Semantic Parsing
The current iteration of the hybrid pipeline relies on standard Optical Character Recognition (`easyocr`) to extract raw strings of text, which are then checked against a static list of illicit keywords (e.g., "Codeine", "LSD"). While effective, this approach is fundamentally brittle. Future iterations should attempt to integrate lightweight Large Language Models (LLMs) or targeted Natural Language Processing (NLP) transformers. Rather than just searching for exact keyword matches, a localized NLP model could semantically understand the *context* of the extracted text, intelligently determining if the text "Take two pills daily" implies a regulated pharmaceutical substance, thereby providing a much deeper layer of semantic safety validation.

### 6.2.4 Ethical Liability and Automation Bias
As automated triage pipelines transition from academic prototypes to active field deployment, the legal system must urgently address the concept of "Automation Bias." Automation bias refers to the psychological propensity of human operators to blindly trust the output of an automated decision-making system, even in the presence of contradictory evidence. In a forensic context, if the hybrid OCR-SVM pipeline confidently flags an image as a narcotic, an overworked human analyst may simply sign off on the classification without conducting a rigorous visual inspection. 

If this "rubber-stamping" leads to a wrongful conviction, the legal liability remains dangerously undefined. Is the individual investigator legally responsible for failing to verify the AI, or does the liability fall on the software engineers who trained the model? Future academic research must work in tandem with legal scholars to establish rigid "human-in-the-loop" verification protocols, mathematically ensuring that AI acts strictly as a triage filter rather than a definitive judicial authority.

### 6.2.5 The Environmental Carbon Footprint of Forensic AI
Finally, the broader environmental impact of digital forensic technology requires critical academic scrutiny. The training and deployment of heavyweight deep learning architectures carry a massive, often overlooked carbon footprint. Training a single 50-layer Convolutional Neural Network on a massive ImageNet dataset utilizing enterprise GPU clusters generates an estimated 284,000 pounds of carbon dioxide equivalent ($CO_{2}e$) emissions—roughly five times the lifetime emissions of an average American car. 

If every regional law enforcement agency internationally attempts to train and deploy bespoke deep learning models for daily digital triage, the cumulative environmental impact will be unsustainable. The classical OpenCV pipeline engineered in this study, which trains its SVM and Random Forest models on standard CPUs in a matter of seconds, represents a highly sustainable, "Green AI" alternative. Future forensic research must prioritize computational efficiency not just as an operational necessity, but as a global environmental imperative, actively shifting the paradigm away from computationally explosive deep learning toward optimized, deterministic mathematics.

### 6.2.6 Integration with Blockchain for Immutable Chain of Custody
While the hybrid OCR-SVM pipeline resolves the issue of visual identification, the legal concept of the "chain of custody" remains a distinct challenge. As established in Chapter 2, traditional cryptographic hashing (MD5/SHA-1) is utilized to prove that evidence has not been tampered with between the point of seizure and the courtroom. However, if an investigator relies on an automated AI pipeline to triage the evidence, defense attorneys frequently argue that the software itself might have imperceptibly corrupted the data during the memory-loading phase.

To preemptively neutralize these legal attacks, future iterations of this triage system should integrate a localized Blockchain ledger. Rather than relying on a vulnerable, centralized database to log which images were flagged as "Weapons" or "Drugs", the system could mathematically package the original image's SHA-256 hash, the 4292-dimensional HOG feature vector, and the final SVM classification output into a single, encrypted block. This block would then be appended to an immutable, decentralized ledger maintained across the local police network. 

Because blockchain relies on sequential cryptographic verification, it becomes mathematically impossible for a rogue investigator (or a malware infection) to retroactively alter a flagged image or change the AI's classification log without invalidating the entire cryptographic chain. By synthesizing deterministic computer vision with blockchain technology, law enforcement can present a "bulletproof" digital audit trail to the court, guaranteeing both the accuracy of the AI and the absolute sanctity of the digital evidence.

### 6.2.7 Policy and Legal Standardization
Finally, future academic work must extend beyond the realm of computer science and cross into legal policy. As hybrid AI systems begin augmenting human investigators, the legal community must establish clear, standardized protocols for admitting machine-assisted triage evidence into court. Research is urgently needed to define exactly how the output of a deterministic SVM or a hybrid OCR pipeline satisfies the Daubert or Frye standards of legal reliability, ensuring that the technological advancements in the laboratory directly translate into successful, transparent prosecutions in the courtroom.

### 6.2.8 Final Concluding Remarks
Ultimately, the transition from manual forensic analysis to automated, deep-learning-driven triage represents both a massive operational leap and a severe legal hazard. As the digital footprint of modern criminal activity continues to expand exponentially, the forensic community must remain critically vigilant. By anchoring future technological advancements in deterministic mathematics, hybrid semantic intelligence, and rigorous constitutional frameworks, law enforcement can successfully mitigate the impending data crisis while simultaneously safeguarding the foundational tenets of justice, equity, and procedural transparency in the courtroom.

## 6.3 References

ACPO, 2012. *ACPO Good Practice Guide for Digital Evidence*. Association of Chief Police Officers and National Police Chiefs' Council (NPCC). Available at: <https://www.digital-detective.net/digital-forensics-documents/ACPO_Good_Practice_Guide_for_Digital_Evidence_v5.pdf> [Accessed 12 February 2026].

Baek, Y., Lee, B., Han, D., Yun, S. and Lee, H., 2019. Character region awareness for text detection. In: *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)*. Long Beach, CA, USA, 15-20 June 2019, pp. 9365-9374. https://doi.org/10.1109/CVPR.2019.00959.

Bay, H., Tuytelaars, T. and Van Gool, L., 2006. SURF: Speeded up robust features. In: A. Leonardis, H. Bischof and A. Pinz, eds. *Computer Vision – ECCV 2006*. Lecture Notes in Computer Science, Vol. 3951. Berlin, Heidelberg: Springer, pp. 404-417. https://doi.org/10.1007/11744023_32.

Bradski, G., 2000. The OpenCV Library. *Dr. Dobb's Journal of Software Tools*, 25(11), pp. 120-125.

Breiman, L., 2001. Random forests. *Machine Learning*, 45(1), pp. 5-32. https://doi.org/10.1023/A:1010933404324.

Cortes, C. and Vapnik, V., 1995. Support-vector networks. *Machine Learning*, 20(3), pp. 273-297. https://doi.org/10.1007/BF00994018.

Cover, T. and Hart, P., 1967. Nearest neighbor pattern classification. *IEEE Transactions on Information Theory*, 13(1), pp. 21-27. https://doi.org/10.1109/TIT.1967.1053964.

Crown Prosecution Service (CPS), 2018. *Review of the Disclosure Process in Criminal Proceedings: The Case of R v Allan*. London: Crown Prosecution Service. Available at: <https://www.cps.gov.uk/publication/review-disclosure-process-criminal-proceedings> [Accessed 14 January 2026].

Dalal, N. and Triggs, B., 2005. Histograms of oriented gradients for human detection. In: *2005 IEEE Computer Society Conference on Computer Vision and Pattern Recognition (CVPR'05)*. San Diego, CA, USA, 20-25 June 2005, Vol. 1, pp. 886-893. https://doi.org/10.1109/CVPR.2005.177.

*Daubert v. Merrell Dow Pharmaceuticals, Inc.*, 1993. 509 U.S. 579, 113 S. Ct. 2786, 125 L. Ed. 2d 469.

Del Mar-Raave, J.R., Bahși, H., Mõru, L. and Hausknecht, K., 2021. A Machine Learning-based Forensic Tool for Image Classification - A Design Science Approach. *Forensic Science International: Digital Investigation*, 38, p. 301265. https://doi.org/10.1016/j.fsidi.2021.301265.

Deng, J., Dong, W., Socher, R., Li, L.J., Li, K. and Fei-Fei, L., 2009. ImageNet: A large-scale hierarchical image database. In: *2009 IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*. Miami, FL, USA, 20-25 June 2009, pp. 248-255. https://doi.org/10.1109/CVPR.2009.5206848.

*Frye v. United States*, 1923. 293 F. 1013 (D.C. Cir.).

Goodfellow, I.J., Shlens, J. and Szegedy, C., 2014. Explaining and harnessing adversarial examples. *arXiv preprint arXiv:1412.6572*. Available at: <https://arxiv.org/abs/1412.6572>.

He, K., Zhang, X., Ren, S. and Sun, J., 2016. Deep residual learning for image recognition. In: *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*. Las Vegas, NV, USA, 27-30 June 2016, pp. 770-778. https://doi.org/10.1109/CVPR.2016.90.

Hotelling, H., 1933. Analysis of a complex of statistical variables into principal components. *Journal of Educational Psychology*, 24(6), pp. 417-441. https://doi.org/10.1037/h0071325.

Howard, A., Sandler, M., Chu, G., Chen, L.C., Chen, B., Tan, M., Wang, W., Zhu, Y., Pang, R., Vasudevan, V. and Le, Q.V., 2019. Searching for MobileNetV3. In: *Proceedings of the IEEE/CVF International Conference on Computer Vision (ICCV)*. Seoul, Korea (South), 27 October - 2 November 2019, pp. 1314-1324. https://doi.org/10.1109/ICCV.2019.00140.

JaidedAI, 2020. *EasyOCR: Ready-to-use OCR with 80+ Supported Languages and All Popular Writing Scripts*. [online] Available at: <https://github.com/JaidedAI/EasyOCR> [Accessed 18 January 2026].

Jolliffe, I.T., 2002. *Principal Component Analysis*. 2nd ed. Springer Series in Statistics. New York: Springer-Verlag.

Kingma, D.P. and Ba, J., 2014. Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*. Available at: <https://arxiv.org/abs/1412.6980>.

Krizhevsky, A., Sutskever, I. and Hinton, G.E., 2012. ImageNet classification with deep convolutional neural networks. In: F. Pereira, C.J. Burges, L. Bottou and K.Q. Weinberger, eds. *Advances in Neural Information Processing Systems (NeurIPS 2012)*. Lake Tahoe, NV, USA, 3-6 December 2012, Vol. 25, pp. 1097-1105.

Locard, E., 1930. The analysis of dust traces. Part I. *American Journal of Police Science*, 1(3), pp. 276-298. https://doi.org/10.2307/1146978.

Lowe, D.G., 2004. Distinctive image features from scale-invariant keypoints. *International Journal of Computer Vision*, 60(2), pp. 91-110. https://doi.org/10.1023/B:VISI.0000029664.99615.94.

Paszke, A., Gross, S., Massa, F., Lerer, A., Bradbury, J., Chanan, G., Killeen, T., Lin, Z., Gimelshein, N., Antiga, L., Desmaison, A., Köpf, A., Yang, E., DeVito, Z., Raison, M., Tejani, A., Sasank, C., Vanschoren, J. and Chintala, S., 2019. PyTorch: An imperative style, high-performance deep learning library. In: H. Wallach, H. Larochelle, A. Beygelzimer, F. d'Alché-Buc, E. Fox and R. Garnett, eds. *Advances in Neural Information Processing Systems (NeurIPS 2019)*. Vancouver, BC, Canada, 8-14 December 2019, Vol. 32, pp. 8024-8035.

Pearson, K., 1901. On lines and planes of closest fit to systems of points in space. *The London, Edinburgh, and Dublin Philosophical Magazine and Journal of Science*, 2(11), pp. 559-572. https://doi.org/10.1080/14786440109462720.

Pedregosa, F., Varoquaux, G., Gramfort, A., Michel, V., Thirion, B., Grisel, O., Blondel, M., Prettenhofer, P., Weiss, R., Dubourg, V., Vanderplas, J., Passos, A., Cournapeau, D., Brucher, M., Perrot, M. and Duchesnay, É., 2011. Scikit-learn: Machine learning in Python. *Journal of Machine Learning Research*, 12, pp. 2825-2830.

Radford, A., Kim, J.W., Hallacy, C., Ramesh, A., Goh, G., Agarwal, S., Sastry, G., Askell, A., Mishkin, P., Clark, J., Krueger, G. and Sutskever, I., 2021. Learning transferable visual models from natural language supervision. In: *Proceedings of the 38th International Conference on Machine Learning (ICML 2021)*. Virtual, 18-24 July 2021, PMLR 139, pp. 8748-8763.

Shi, B., Bai, X. and Yao, C., 2016. An end-to-end trainable neural network for image-based sequence recognition and its application to scene text recognition. *IEEE Transactions on Pattern Analysis and Machine Intelligence*, 39(11), pp. 2298-2304. https://doi.org/10.1109/TPAMI.2016.2646371.

Simonyan, K. and Zisserman, A., 2014. Very deep convolutional networks for large-scale image recognition. *arXiv preprint arXiv:1409.1556*. Available at: <https://arxiv.org/abs/1409.1556>.

Stevens, M., Bursztein, E., Karpman, P., Albertini, A. and Markov, Y., 2017. The first collision for full SHA-1. In: J. Katz and H. Shacham, eds. *Advances in Cryptology – CRYPTO 2017*. Lecture Notes in Computer Science, Vol. 10401. Cham: Springer, pp. 570-596. https://doi.org/10.1007/978-3-319-63688-7_19.
