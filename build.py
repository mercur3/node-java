#!/usr/bin/python3

SUPPORTED_JAVA_VERSIONS: list[int] = [21]
#SUPPORTED_NODE_VERSIONS: list[int] = [18, 20, 21]
SUPPORTED_FEDORA_VERSIONS: list[str] = [41]

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
        for n in SUPPORTED_FEDORA_VERSIONS:
            #for d in SUPPORTED_DEBIAN_VERSIONS:
                tag_name = f"node-java:fedora{n}-java{j}"
                src_tag_name = f"fedora:{n}"
                output += f"""
  - job:
    displayName: Building image on Fedora {n}, Java {j}
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

      - task: Docker@2
        displayName: Build & Push Node‐Java Image
        condition: not(eq(variables['Build.Reason'], 'PullRequest'))
        inputs:
          command: buildAndPush
          containerRegistry: docker-hub-login
          repository: mercur3/node-java
          Dockerfile: Dockerfile
          tags: |
            fedora{n}-java{j}
            latest

"""
    with open("azure-pipelines.yml", "w") as fd:
        output += "\n"
        print(output)
        fd.write(output)

if __name__ == "__main__":
    main()

