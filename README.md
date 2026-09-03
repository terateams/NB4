# netbox-docker

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/netbox-community/netbox-docker)][github-release]
[![GitHub stars](https://img.shields.io/github/stars/netbox-community/netbox-docker)][github-stargazers]
![GitHub closed pull requests](https://img.shields.io/github/issues-pr-closed-raw/netbox-community/netbox-docker)
![Github release workflow](https://img.shields.io/github/actions/workflow/status/netbox-community/netbox-docker/release.yml?branch=release)
![Docker Pulls](https://img.shields.io/docker/pulls/netboxcommunity/netbox)
[![GitHub license](https://img.shields.io/github/license/netbox-community/netbox-docker)][netbox-docker-license]

[The GitHub repository][netbox-docker-github] houses the components needed to build NetBox as a container.
Images are built regularly using the code in that repository
and are pushed to [Docker Hub][netbox-dockerhub],
[Quay.io][netbox-quayio] and [GitHub Container Registry][netbox-ghcr].
_NetBox Docker_ is a project developed and maintained by the _NetBox_ community.

Do you have any questions?
Before opening an issue on GitHub,
please join [our Slack][netbox-docker-slack]
and ask for help in the [`#netbox-docker`][netbox-docker-slack-channel] channel,
or start a new [GitHub Discussion][github-discussions].

[github-stargazers]: https://github.com/netbox-community/netbox-docker/stargazers
[github-release]: https://github.com/netbox-community/netbox-docker/releases
[netbox-dockerhub]: https://hub.docker.com/r/netboxcommunity/netbox/
[netbox-quayio]: https://quay.io/repository/netboxcommunity/netbox
[netbox-ghcr]: https://github.com/netbox-community/netbox-docker/pkgs/container/netbox
[netbox-docker-github]: https://github.com/netbox-community/netbox-docker/
[netbox-docker-slack]: https://join.slack.com/t/netdev-community/shared_invite/zt-mtts8g0n-Sm6Wutn62q_M4OdsaIycrQ
[netbox-docker-slack-channel]: https://netdev-community.slack.com/archives/C01P0GEVBU7
[netbox-slack-channel]: https://netdev-community.slack.com/archives/C01P0FRSXRV
[netbox-docker-license]: https://github.com/netbox-community/netbox-docker/blob/release/LICENSE
[github-discussions]: https://github.com/netbox-community/netbox-docker/discussions

## Quickstart

To get _NetBox Docker_ up and running run the following commands.
There is a more complete [_Getting Started_ guide on our wiki][wiki-getting-started] which explains every step.

```bash
git clone -b release https://github.com/netbox-community/netbox-docker.git
cd netbox-docker
# Copy the example override file
cp docker-compose.override.yml.example docker-compose.override.yml
# Read and edit the file to your liking
docker compose pull
docker compose up
```

The whole application will be available after a few minutes.
Open the URL `http://0.0.0.0:8000/` in a web-browser.
You should see the NetBox homepage.

To create the first admin user run this command:

```bash
docker compose exec netbox /opt/netbox/netbox/manage.py createsuperuser
```

If you need to restart Netbox from an empty database often,
you can also set the `SUPERUSER_*` variables in your `docker-compose.override.yml`.

[wiki-getting-started]: https://github.com/netbox-community/netbox-docker/wiki/Getting-Started

## Container Image Tags

New container images are built and published automatically every ~24h.

> We recommend to use either the `vX.Y.Z-a.b.c` tags or the `vX.Y-a.b.c` tags in production!

- `vX.Y.Z-a.b.c`, `vX.Y-a.b.c`:
  These are release builds containing _NetBox version_ `vX.Y.Z`.
  They contain the support files of _NetBox Docker version_ `a.b.c`.
  You must use _NetBox Docker version_ `a.b.c` to guarantee the compatibility.
  These images are automatically built from [the corresponding releases of NetBox][netbox-releases].
- `latest-a.b.c`:
  These are release builds, containing the latest stable version of NetBox.
  They contain the support files of _NetBox Docker version_ `a.b.c`.
  You must use _NetBox Docker version_ `a.b.c` to guarantee the compatibility.
- `snapshot-a.b.c`:
  These are prerelease builds.
  They contain the support files of _NetBox Docker version_ `a.b.c`.
  You must use _NetBox Docker version_ `a.b.c` to guarantee the compatibility.
  These images are automatically built from the [`main` branch of NetBox][netbox-main].

For each of the above tag, there is an extra tag:

- `vX.Y.Z`, `vX.Y`:
  This is the same version as `vX.Y.Z-a.b.c` (or `vX.Y-a.b.c`, respectively).
- `latest`
  This is the same version as `latest-a.b.c`.
  It always points to the latest version of _NetBox Docker_.
- `snapshot`
  This is the same version as `snapshot-a.b.c`.
  It always points to the latest version of _NetBox Docker_.

[netbox-releases]: https://github.com/netbox-community/netbox/releases
[netbox-main]: https://github.com/netbox-community/netbox/tree/main

## Documentation

Please refer [to our wiki on GitHub][netbox-docker-wiki] for further information on how to use the NetBox Docker image properly.
The wiki covers advanced topics such as using files for secrets, configuring TLS, deployment to Kubernetes, monitoring and configuring LDAP.

Our wiki is a community effort.
Feel free to correct errors, update outdated information or provide additional guides and insights.

[netbox-docker-wiki]: https://github.com/netbox-community/netbox-docker/wiki/

## Getting Help

Feel free to ask questions in our [GitHub Community][netbox-community]
or [join our Slack][netbox-docker-slack] and ask [in our channel `#netbox-docker`][netbox-docker-slack-channel],
which is free to use and where there are almost always people online that can help you.

If you need help with using NetBox or developing for it or against it's API
you may find [the `#netbox` channel][netbox-slack-channel] on the same Slack instance very helpful.

[netbox-community]: https://github.com/netbox-community/netbox-docker/discussions

## Dependencies

This project relies only on _Docker_ and _docker-compose_ meeting these requirements:

- The _Docker version_ must be at least `20.10.10`.
- The _containerd version_ must be at least `1.5.6`.
- The _docker-compose version_ must be at least `1.28.0`.

To check the version installed on your system run `docker --version` and `docker compose version`.

## Updating

### 内部部署分支

本仓库是 NetBox Docker 的 Fork，并包含内部部署定制。

- `release` 镜像同步 `netbox-community/netbox-docker:release`。仅可在此分支使用
  GitHub 的 **Sync fork**。
- `production` 包含内部插件和部署定制，生产环境应从此分支部署。
- 不要使用 Fork 同步弹窗中的 **Contribute** 或 **Open pull request**；这两个操作会
  向上游官方仓库创建 PR。

要引入上游发布版本，先同步 `release`，再从 `production` 创建临时分支并合并
`release`，最后仅在本仓库内创建 PR：

```bash
git switch production
git pull --ff-only origin production
git switch -c chore/merge-upstream-<netbox-version>
git fetch origin
git merge origin/release

# 解决冲突，并在创建 PR 前验证定制镜像。
docker compose config
docker compose build --pull netbox netbox-worker

git push -u origin chore/merge-upstream-<netbox-version>
```

将 `chore/merge-upstream-<netbox-version>` 合并到 `production`。重新构建和重启
服务前，务必先备份部署数据。

### PostgreSQL 大版本与数据卷升级

上游镜像升级可能同时升级 PostgreSQL 主版本，或修改 Compose 的数据卷名称和挂载路径。
此类变更下，即使 `docker compose up -d` 和 NetBox 健康检查均成功，也可能是 Compose
创建并连接到了一个新的空数据库，而不是原有数据卷。

在将升级部署到生产前，必须在本地副本完成一次包含真实数据库数据的演练：

1. 对比升级前后 `docker-compose.yml` 中 `postgres` 的镜像版本、卷名称和挂载路径。
2. 从 `backups/` 或已验证的异地备份取得最新的逻辑转储文件（`.dump`）。
3. 在新 PostgreSQL 版本中恢复备份，再启动 NetBox 以执行核心及插件数据库迁移。
4. 核对用户、设备、IP 地址和关键插件数据的数量，再切换生产环境。

PostgreSQL 主版本之间不能直接复用数据目录。例如，不能将 PostgreSQL 17 的数据卷直接
挂载到 PostgreSQL 18 容器。应使用之前生成的逻辑备份恢复到新版本；详见上游
[PostgreSQL Update 指引][netbox-docker-wiki-postgresql-update]。恢复期间不要运行
`docker compose down -v`、`docker volume rm` 或 `docker system prune --volumes`。

以下示例将 `backups/` 目录中的数据库转储恢复到当前 PostgreSQL 18 服务。先选择要恢复的
备份，并验证它是 PostgreSQL 自定义格式的有效逻辑转储：

```bash
export BACKUP_FILE=backups/<netbox-database-backup>.dump
test -s "$BACKUP_FILE"
docker run --rm -i docker.io/postgres:18-alpine pg_restore --list < "$BACKUP_FILE" \
  >/dev/null
```

校验成功后，停止 NetBox 和 worker，避免它们在恢复过程中访问数据库；不要删除数据库卷。
仅启动新 Compose 的 PostgreSQL 服务。恢复前会删除并重建当前 `netbox` 数据库，因此必须
确认当前数据库没有需要保留的数据。不要使用 `pg_restore --clean` 覆盖一个已执行新版插件
迁移的数据库：备份外的插件表可能依赖核心表，导致删除顺序冲突并留下部分恢复的数据。

```bash
docker compose stop netbox netbox-worker
docker compose up -d postgres

# 终止现有连接，然后从维护数据库重建一个空的 NetBox 数据库。
docker compose exec -T postgres sh -c \
  'psql -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d postgres -c \
  "SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '\''$POSTGRES_DB'\'' AND pid <> pg_backend_pid();"'
docker compose exec -T postgres sh -c \
  'dropdb -U "$POSTGRES_USER" "$POSTGRES_DB" && createdb -U "$POSTGRES_USER" "$POSTGRES_DB"'

cat "$BACKUP_FILE" | \
  docker compose exec -T postgres sh -c \
  'pg_restore -U "$POSTGRES_USER" -d "$POSTGRES_DB" --exit-on-error --no-owner'

# NetBox 启动后会执行核心及插件迁移。
docker compose up -d
```

恢复完成后，应登录并核对用户、设备、IP 地址及关键插件数据，再决定是否删除临时副本。
在验证完成前，保留原始 `.dump` 文件及对应的媒体备份。

Please read [the release notes][releases] carefully when updating to a new image version.
Note that the version of the NetBox Docker container image must stay in sync with the version of the Git repository.

If you update for the first time, be sure [to follow our _How To Update NetBox Docker_ guide in the wiki][netbox-docker-wiki-updating].

[releases]: https://github.com/netbox-community/netbox-docker/releases
[netbox-docker-wiki-updating]: https://github.com/netbox-community/netbox-docker/wiki/Updating
[netbox-docker-wiki-postgresql-update]: https://github.com/netbox-community/netbox-docker/wiki/Updating#postgresql-update

## Rebuilding the Image

`./build.sh` can be used to rebuild the container image.
See `./build.sh --help` for more information or `./build-latest.sh` for an example.

For more details on custom builds [consult our wiki][netbox-docker-wiki-build].

[netbox-docker-wiki-build]: https://github.com/netbox-community/netbox-docker/wiki/Build

## Tests

We have a test script.
It runs NetBox's own unit tests and ensures that NetBox starts:

```bash
IMAGE=docker.io/netboxcommunity/netbox:latest ./test.sh
```

## Support

This repository is currently maintained by the community.
The community is expected to help each other.

Please consider sponsoring the maintainers of this project.
