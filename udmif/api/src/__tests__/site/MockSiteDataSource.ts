import { GraphQLDataSource } from 'apollo-datasource-graphql/dist/GraphQLDataSource';
import { Site, SitesResponse } from '../../site/model';
import { createSites } from './data';

export default class MockSiteDataSource extends GraphQLDataSource<object> {
  constructor() {
    super();
  }

  public initialize(config) {
    super.initialize(config);
  }

  async getSites(): Promise<SitesResponse> {
    const sites: Site[] = createSites(30);
    return { sites, totalCount: 30, totalFilteredCount: 10 };
  }

  async getSiteNames(): Promise<string[]> {
    return createSites(10)
      .map((d) => d.name)
      .sort();
  }

  async getSite(): Promise<Site> {
    return createSites(1)[0];
  }
}
