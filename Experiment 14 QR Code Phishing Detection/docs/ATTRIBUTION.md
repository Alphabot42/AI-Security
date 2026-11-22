# Sources and attribution

## Dataset and original study

Fouad Trad and Ali Chehab. **Detecting Quishing Attacks with Machine Learning
Techniques Through QR Code Analysis** (2025).

- Paper: https://arxiv.org/abs/2505.03451
- Authors' dataset repository: https://github.com/fouadtrad/Detecting-Quishing-Attacks-with-Machine-Learning-Techniques-Through-QR-Code-Analysis
- Upstream license: https://github.com/fouadtrad/Detecting-Quishing-Attacks-with-Machine-Learning-Techniques-Through-QR-Code-Analysis/blob/main/LICENSE
- CC BY 4.0: https://creativecommons.org/licenses/by/4.0/

The upstream repository's license was checked during publication preparation.
The two arrays contain the source images and labels. The study selects records,
creates experiment memberships, generates representation variants and transformed
or regenerated QR fixtures, and derives model outputs and summary statistics.
These changes do not imply endorsement by the dataset authors.

The raw dataset is obtained from its authors rather than duplicated here.
Its attribution must accompany any subsequently released dataset-derived fixtures.
The upstream license applies to that material, not automatically to every
independent source file in this repository.

## Course reference

The reference QRClassifier architecture was reconstructed from Hamza Kondah's
course material. The original trained weights and exact training settings were
unavailable. The notebooks therefore implement a reference with the recovered
architecture; they do not claim exact parity with the instructor's scores.
Course PDFs and private course question-and-answer material are not included.

## Established methods

- Madry et al. **Towards Deep Learning Models Resistant to Adversarial Attacks**:
  https://arxiv.org/abs/1706.06083
- Moosavi-Dezfooli, Fawzi and Frossard. **DeepFool**:
  https://arxiv.org/abs/1511.04599
- Athalye, Carlini and Wagner. **Obfuscated Gradients Give a False Sense of Security**:
  https://proceedings.mlr.press/v80/athalye18a.html
- Zhang et al. **Theoretically Principled Trade-off between Robustness and Accuracy**:
  https://proceedings.mlr.press/v97/zhang19p.html
- RFC 3986, unreserved characters and syntax-based normalization:
  https://www.rfc-editor.org/rfc/rfc3986.html

The implementations are study-specific experiments. A named established method
does not validate this study's measurements or certify its detector.

## Authorship and assistance

Natacha executed the experiments on Cube-AI and supplied the recorded notebooks.
ChatGPT substantially assisted in writing code and explanations. Claude and Kimi
were also used to discuss candidate ideas. The notebooks and report record
successful checks, failed approaches, methodological corrections and remaining
limits. AI assistance is disclosed without assigning originality to established
methods or the upstream dataset.
