import type { Core } from '@strapi/strapi';

export default {
  register({ strapi }: { strapi: Core.Strapi }) {},

  async bootstrap({ strapi }: { strapi: Core.Strapi }) {
    try {
      const plugin = strapi.plugin('users-permissions');
      if (!plugin) {
        strapi.log.warn('users-permissions plugin not available');
        return;
      }

      const roles = await strapi.documents('plugin::users-permissions.role').findMany();
      const publicRole = roles.find((r: Record<string, unknown>) => r.type === 'public');

      if (!publicRole) {
        strapi.log.warn('Public role not found');
        return;
      }

      strapi.log.info(`Found public role: ${publicRole.id} - ${publicRole.name}`);

      const permissions = [
        { action: 'api::tour.tour.find', role: publicRole.id },
        { action: 'api::tour.tour.findOne', role: publicRole.id },
        { action: 'api::category.category.find', role: publicRole.id },
        { action: 'api::category.category.findOne', role: publicRole.id },
        { action: 'api::type.type.find', role: publicRole.id },
        { action: 'api::type.type.findOne', role: publicRole.id },
      ];

      for (const perm of permissions) {
        try {
          await strapi.documents('plugin::users-permissions.permission').create({
            data: perm,
            status: 'published',
          });
          strapi.log.info(`Granted: ${perm.action}`);
        } catch (e) {
          // Permission already exists, that's fine
          strapi.log.info(`Already exists: ${perm.action}`);
        }
      }

      strapi.log.info('Public permissions configured successfully');
    } catch (error) {
      strapi.log.error('Failed to set public permissions:');
      strapi.log.error(error);
    }
  },
};
