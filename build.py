#!/usr/bin/python3

SUPPORTED_JAVA_VERSIONS: list[int] = [11, 17]
SUPPORTED_NODE_VERSIONS: list[int] = [16, 18, 19, 20]
SUPPORTED_DEBIAN_VERSIONS: list[str] = ["bullseye"]

def main() -> None:
    output = """
###############################################################################
# WARNING                                                                     #
# This file is autogenerated. Do NOT edit this file. Run =./build.py= instead #
###############################################################################

trigger:
  - master
pr:
  autoCancel: true
  branches:
    include:
      - master
pool:
  vmImage: ubuntu-latest
jobs:"""

    for j in SUPPORTED_JAVA_VERSIONS:
        for n in SUPPORTED_NODE_VERSIONS:
            for d in SUPPORTED_DEBIAN_VERSIONS:
                tag_name = f"node-java:node{n}-java{j}-{d}"
                src_tag_name = f"node:{n}-{d}"
                output += f"""
  - job:
    displayName: Building image on Debian {d}, Java {j}, Node {n}
    pool:
      vmImage: ubuntu-latest
    steps:
      - script: |
          echo "Building the images"
          printf "Using %d threads\\n" $(nproc)
          echo "------------------------------------------------------\\n"
          sed "s/__src_tag_name__/{src_tag_name}/g" -i Dockerfile
          sed "s/__java_version__/{j}/g" -i Dockerfile
          cat Dockerfile
        displayName: Adding the version

      - script: |
          set -e
          docker build -f Dockerfile -t mercur3/{tag_name} .
          echo "------------------------------------------------------\\n"
        displayName: docker build -f Dockerfile -t mercur3/{tag_name} .

      - script: |
          echo "------------------------------------------------------\\n"
          echo "$DOCKER_PASSWORD" | docker login -u mercur3 --password-stdin
          docker push mercur3/{tag_name}
        displayName: docker push mercur3/{tag_name}
        condition: not(eq(variables['Build.Reason'], 'PullRequest'))
        env:
          DOCKER_PASSWORD: $(DOCKER_PASSWORD)

"""
    with open("azure-pipelines.yml", "w") as fd:
        output += "\n"
        print(output)
        fd.write(output)

if __name__ == "__main__":
    main()

